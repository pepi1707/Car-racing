import tensorflow as tf
import numpy as np
import time
import gym
from gym.spaces import Discrete, Box
import Car_Environment



def train(env_name = 'CartPole-v0', actor_sizes = [32], critic_sizes = [32], num_batches = 50,
          epochs = 50, gamma = 0.99, pi_lr = 0.0003, vf_lr = 0.001, lam = 0.97, visualize = 1,
          train_v_iters = 80, max_ep_len = 5000):
        
    def mlp(x, sizes, activations):
        #x = tf.layers.conv2d(inputs = x, filters = sizes[0], kernel_size = (5,5), strides = 1, padding = 'valid', activation = tf.nn.relu)
        #x = tf.layers.max_pooling2d(inputs = x, pool_size = (2, 2), strides = (1, 1), padding = 'valid')
        x = tf.layers.flatten(x)
        for idx, size in enumerate(sizes):
            x = tf.layers.dense(x, units = size, activation = activations[idx])
        return x

    env = Car_Environment.Car_Environment()
    #assert isinstance(env.observation_space, Box), \
    #    "This example only works for envs with continuous state spaces."
    #assert isinstance(env.action_space, Discrete), \
    #    "This example only works for envs with discrete action spaces."

    obs_dim = 7 #env.observation_space.shape
    input_shape = (None, obs_dim)
    single_input_shape = (1, obs_dim)
    n_acts = 3 #env.action_space.n

    #build actor

    obs_ph = tf.placeholder(dtype = tf.float32, shape = input_shape)
    logits = mlp(x = obs_ph, sizes = actor_sizes + [n_acts], activations = [tf.nn.relu, None])

    actions = tf.squeeze(tf.multinomial(logits = logits, num_samples = 1), axis = 1)

    weights_ph = tf.placeholder(dtype = tf.float32, shape = (None, ))
    actions_ph = tf.placeholder(dtype = tf.int32, shape = (None, ))
    actions_mask = tf.one_hot(actions_ph, n_acts)
    probs = actions_mask * tf.nn.log_softmax(logits)

    log_probs = tf.reduce_sum(probs, axis = 1)
    actor_loss = -tf.reduce_sum(log_probs * weights_ph) / num_batches

    train_actor = tf.train.AdamOptimizer(learning_rate = pi_lr).minimize(actor_loss)

    #build critic

    obs_cr = tf.placeholder(dtype = tf.float32, shape = input_shape)
    output_cr = mlp(x = obs_cr, sizes = critic_sizes + [1], activations = [tf.nn.relu, None])
    value_cr = tf.reduce_sum(output_cr, axis = 1)
    output = tf.placeholder(dtype = tf.float32, shape = (None, ))
    loss_cr = tf.reduce_mean((value_cr - output) ** 2)

    train_cr = tf.train.GradientDescentOptimizer(learning_rate = vf_lr).minimize(loss_cr)


    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        
        def calc_vf(rewards):
            vf = np.zeros_like(rewards)
            reward = 0
            for i in reversed(range(len(rewards))):
                reward += rewards[i]
                vf[i] = reward
                reward *= gamma
            return vf

        def calc_adv(tds):
            adv = np.zeros_like(tds)
            cur = 0
            for i in reversed(range(len(tds))):
                cur += tds[i]
                adv[i] = cur
                cur *= lam * gamma
            return adv

        def calc_td(obs, rewards, last_val):
            tds = np.zeros_like(rewards)
            for i in range(len(obs)):
                vst_0 = sess.run(value_cr, {obs_cr : obs[i].reshape(single_input_shape)})[0]
                if i == len(obs) - 1:
                    vst_1 = last_val
                else:
                    vst_1 = sess.run(value_cr, {obs_cr : obs[i + 1].reshape(single_input_shape)})[0]
                tds[i] = rewards[i] + gamma * vst_1 - vst_0
            return tds

        def train_one_epoch():

            batch_obs = []
            batch_ret = []
            batch_weights = []
            batch_lens = []
            batch_acts = []
            batch_vf = []

            while len(batch_lens) < num_batches:
                ep_rews = []
                ep_obs = []
                obs = env.reset()
                done = False

                while not done and len(ep_obs) < 5000:
                    ep_obs.append(obs.copy())
                    act = sess.run(actions, {obs_ph : obs.reshape(single_input_shape)})[0]
                    obs, rew, done, _ = env.step(act)

                    batch_acts.append(act)
                    ep_rews.append(rew)

                batch_lens.append(len(ep_rews))
                batch_ret.append(sum(ep_rews))
                
                batch_obs.extend(ep_obs)
                ep_tds = list(calc_td(obs = ep_obs, rewards = ep_rews, last_val = 0))
                ep_weights = list(calc_adv(tds = ep_tds))
                batch_weights.extend(ep_weights)

                ep_vf = list(calc_vf(rewards = ep_rews))
                batch_vf.extend(ep_vf)            

            batch_actor_loss, _ = sess.run([actor_loss, train_actor], feed_dict = {
                                            obs_ph: np.array(batch_obs),
                                            actions_ph: np.array(batch_acts),
                                            weights_ph: np.array(batch_weights)
                                        })
            
            epoch_critic_loss = 0
            input_dict = {obs_cr : np.array(batch_obs), output: np.array(batch_vf)}
            for _ in range(train_v_iters):
                batch_critic_loss, _, value_cr_t = sess.run([loss_cr, train_cr, value_cr], feed_dict = input_dict)
                epoch_critic_loss += batch_critic_loss
            
            epoch_critic_loss /= train_v_iters
            #print(value_cr_t)
            
            rand_added = 1 if np.random.random_sample() < visualize - int(visualize) else 0
            env.render()
            for i in range(int(visualize) + rand_added):
                obs = env.reset()
                cnt = 0

                while True:
                    cnt += 1
                    act = sess.run(actions, {obs_ph : obs.reshape(single_input_shape)})[0]
                    obs, _, done, _ = env.step(act)
                    time.sleep(0.01)

                    if done or cnt >=  5000:
                        break
            env.endRender()
            return batch_actor_loss, epoch_critic_loss, batch_ret, batch_lens

        for i in range(epochs):
            batch_loss_act, batch_loss_cr, batch_rets, batch_lens = train_one_epoch()
            print('epoch: %3d \t actor loss: %.3f \t critic loss: %.3f \t return: %.3f \t ep_len: %.3f \t max_len: %.3f'%
                (i + 1, batch_loss_act, batch_loss_cr, np.mean(batch_rets), np.mean(batch_lens), np.max(batch_lens)))

if __name__ == '__main__':
    train(env_name = 'Pong-v0', actor_sizes = [64], critic_sizes = [64], num_batches = 10,
          epochs = 5000, gamma = 0.99, pi_lr = 1e-3, vf_lr = 1e-3, lam = 0.97, visualize = 1,
          train_v_iters = 20)



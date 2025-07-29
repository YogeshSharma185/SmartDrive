from stable_baselines3 import PPO
from src.game.driving_rl_wrapper import DrivingRLWrapper

def main():
    env = DrivingRLWrapper(render_mode=False)

    model = PPO("CnnPolicy", env, verbose=1)
    model.learn(total_timesteps=100_000)
    model.save("ppo_speak2steer")

    env.close()

if __name__ == "__main__":
    main()

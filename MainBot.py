import sc2
from sc2 import Race, Difficulty, maps, run_game, position, Result
from sc2.player import Bot, Computer
import asyncio

class MainBot(sc2.BotAI):
    async def on_step(self, iteration):
        self.iteration = iteration
        await self.distribute_workers()

    async def distribute_workers(self, resource_ratio: float = 2):
        return await super().distribute_workers(resource_ratio)
    

def main():
    run_game(maps.get("PortAleksanderLE"), [Bot(Race.Protoss, MainBot()), Computer(Race.Protoss, Difficulty.Medium)], realtime = False)

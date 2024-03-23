import sc2
from sc2 import Race, Difficulty, maps, run_game, position, Result
from sc2.player import Bot, Computer
import asyncio
import random

class MainBot(sc2.BotAI):
    async def on_step(self, iteration):
        self.iteration = iteration
        await self.distribute_workers()

    async def distribute_workers(self, resource_ratio: float = 2):
        return await super().distribute_workers(resource_ratio)
    

def mapRandomizer():
    mapSelected = [maps.get("AutomatonLE"), maps.get("PortAleksanderLE"),
            maps.get("YearZeroLE"), maps.get("AcropolisLE"),
            maps.get("ThunderbirdLE"), maps.get("TurboCruise'84LE"),
            maps.get("CyberForestLE"), maps.get("KairosJunctionLE"),
            maps.get("KingsCoveLE"), maps.get("NewRepugnancyLE")]
    mapToSend = mapSelected[random.randint(0, len(mapSelected) - 1)]
    print(str(mapToSend))
    return mapToSend

def main():
    run_game(mapRandomizer(), [Bot(Race.Protoss, MainBot()), Computer(Race.Protoss, Difficulty.Medium)], realtime = False)

if __name__ == "__main__":
    main()
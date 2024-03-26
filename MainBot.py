import sc2
from sc2 import Race, Difficulty, maps, run_game, position, Result
from sc2.player import Bot, Computer
import asyncio
import random

class MainBot(sc2.BotAI):
    async def on_step(self, iteration):
        self.iteration = iteration
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.build_gateway()
        await self.build_cybernetics_core()

    async def distribute_workers(self, resource_ratio: float = 2):
        return await super().distribute_workers(resource_ratio)
    
    async def build_workers(self):
        for nexus in self.units(sc2.UnitTypeId.NEXUS).ready.noqueue:
            if self.can_afford(sc2.UnitTypeId.PROBE):
                await self.do(nexus.train(sc2.UnitTypeId.PROBE))
    
    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(sc2.UnitTypeId.PYLON):
            nexuses = self.units(sc2.UnitTypeId.NEXUS).ready
            if nexuses.exists:
                if self.can_afford(sc2.UnitTypeId.PYLON):
                    await self.build(sc2.UnitTypeId.PYLON, near=nexuses.first)
    
    async def build_assimilators(self):
        for nexus in self.units(sc2.UnitTypeId.NEXUS).ready.noqueue:
            vespenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vespene in vespenes:
                if not self.can_afford(sc2.UnitTypeId.ASSIMILATOR):
                    break
                worker = self.select_build_worker(vespene.position)
                if worker is None:
                    break
                if not self.units(sc2.UnitTypeId.ASSIMILATOR).closer_than(1.0, vespene).exists:
                    await self.do(worker.build(sc2.UnitTypeId.ASSIMILATOR, vespene))

    async def build_gateway(self):
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.units(sc2.UnitTypeId.PYLON).ready.random
            if self.units(sc2.UnitTypeId.GATEWAY).ready.exists:
                if self.can_afford(sc2.UnitTypeId.GATEWAY):
                    await self.build(sc2.UnitTypeId.GATEWAY, near=pylon)
            else:
                if self.can_afford(sc2.UnitTypeId.GATEWAY):
                    await self.build(sc2.UnitTypeId.GATEWAY, near=pylon)

    async def build_cybernetics_core(self):
        if self.units(sc2.UnitTypeId.GATEWAY).ready.exists:
            gateway = self.units(sc2.UnitTypeId.GATEWAY).ready.random
            if self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists:
                if self.can_afford(sc2.UnitTypeId.CYBERNETICSCORE):
                    await self.build(sc2.UnitTypeId.CYBERNETICSCORE, near=gateway)
            else:
                if self.can_afford(sc2.UnitTypeId.CYBERNETICSCORE):
                    await self.build(sc2.UnitTypeId.CYBERNETICSCORE, near=gateway)
    

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
    run_game(mapRandomizer(), [Bot(Race.Protoss, MainBot()), Computer(Race.Protoss, Difficulty.Easy)], realtime = False)

if __name__ == "__main__":
    main()
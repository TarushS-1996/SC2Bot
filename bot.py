import sc2
from sc2 import Race, Difficulty, maps, run_game, position, Result
from sc2.player import Computer, Bot
from sc2.constants import NEXUS, PROBE, STALKER, PYLON, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, STARGATE, VOIDRAY, OBSERVER, ROBOTICSFACILITY, ZEALOT, AbilityId, ADEPT, HIGHTEMPLAR, IMMORTAL
import random
import cv2
import numpy as np 
import time
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

class AIbot(sc2.BotAI):
	def __init__(self):
		self.ITERATION_PER_MINUTE = 165
		self.MAX_WORKERS = 30
		self.do_something_after = 0
		self.train_data = []

	def on_end(self, game_result):
		print(game_result)
		if game_result == Result.Victory:
			np.save("Data/TrainData/{}.npy".format(str(int(time.time()))), np.array(self.train_data))

	async def on_step(self, iteration):
		self.iteration = iteration
		await self.scout()
		await self.distribute_workers()
		await self.build_workers()
		await self.build_pylons()
		await self.build_assimilators()
		#await self.morph_gateway()
		await self.expand()
		await self.buildings_offensive()
		await self.forces()
		await self.forces2()
		await self.forces3()
		await self.forces4()
		await self.forces5()
		await self.intel()
		await self.attack()

	def random_location_variance(self, enemy_start_location):
		x = enemy_start_location[0]
		y = enemy_start_location[1]

		x += ((random.randrange(-20, 20))/100) * enemy_start_location[0]
		y += ((random.randrange(-20, 20))/100) * enemy_start_location[1]

		if x < 0:
			x = 0
		if y < 0:
			y = 0
		if x > self.game_info.map_size[0]:
			x = self.game_info.map_size[0]
		if y > self.game_info.map_size[1]:
			y = self.game_info.map_size[1]

		go_to = position.Point2(position.Pointlike((x,y)))
		return go_to

	async def scout(self):
		if len(self.units(OBSERVER)) > 0:
			scout = self.units(OBSERVER)[0]
			if scout.is_idle:
				enemy_location = self.enemy_start_locations[0]
				move_to = self.random_location_variance(enemy_location)
				#print(move_to)
				await self.do(scout.move(move_to))

		else:
			for rf in self.units(ROBOTICSFACILITY).ready.noqueue:
				if self.can_afford(OBSERVER) and self.supply_left > 0:
					await self.do(rf.train(OBSERVER))

	async def intel(self):
		game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)
		draw_dict = {NEXUS: [15, (255, 0, 0)], PROBE: [1, (0, 255, 0)], PYLON: [2, (0, 25, 25)], ASSIMILATOR: [3, (10, 55, 150)], GATEWAY: [3, (50, 150, 0)], CYBERNETICSCORE: [3, (55, 25, 55)], STARGATE: [3, (75, 100, 30)], VOIDRAY: [3, (30, 255, 150)], ROBOTICSFACILITY: [3, (215, 155, 0)], STALKER: [3, (40, 210, 100)], ZEALOT: [2, (10, 10, 215)], ADEPT: [2, (215, 175, 55)], IMMORTAL: [3, (55, 175, 215)]}
		for unit_type in draw_dict:
			for unit in self.units(unit_type).ready:
				pos = unit.position
				cv2.circle(game_data, (int(pos[0]), int(pos[1])), draw_dict[unit_type][0], draw_dict[unit_type][1], -1)
		
		main_base_name = ["nexus", "commandcenter", "hatchery"]
		for enemy_building in self.known_enemy_structures:
			pos = enemy_building.position
			if enemy_building.name.lower() not in main_base_name:
				cv2.circle(game_data, (int(pos[0]), int(pos[1])), 5, (200, 50, 212), -1)

		for enemy_building in self.known_enemy_structures:
			pos = enemy_building.position
			if enemy_building.name.lower() in main_base_name:
				cv2.circle(game_data, (int(pos[0]), int(pos[1])), 15, (0, 0, 255), -1)

		for enemy_unit in self.known_enemy_units:
			if not enemy_unit.is_structure:
				worker_name = ["probe", "scv", "drone"]
				pos = enemy_unit.position
				if enemy_unit.name.lower() in worker_name:
					cv2.circle(game_data, (int(pos[0]), int(pos[1])), 1, (55, 0, 155), -1)
				else: 
					cv2.circle(game_data, (int(pos[0]), int(pos[1])), 3, (50, 0, 215), -1)
		for obs in self.units(OBSERVER).ready:
			pos = obs.position
			cv2.circle(game_data, (int(pos[0]), int(pos[1])), 1, (255, 255, 255), -1)


		line_max = 50
		mineral_ratio = self.minerals / 1500
		if mineral_ratio > 1.0:
			mineral_ratio = 1

		vaspene_ratio = self.vespene / 1500
		if vaspene_ratio > 1.0:
			vaspene_ratio = 1

		population_ratio = self.supply_left / self.supply_cap
		if population_ratio > 1.0:
			population_ratio = 1.0

		plausible_supply = self.supply_cap / 200.0

		military_raio_voidray = len(self.units(VOIDRAY)) / 10
		if military_raio_voidray > 1.0:
			military_raio_voidray = 1

		military_raio_stalker = len(self.units(STALKER)) / 10
		if military_raio_stalker > 1.0:
			military_raio_stalker = 1

		military_raio_adept = len(self.units(ADEPT)) / 10
		if military_raio_adept > 1.0:
			military_raio_adept = 1

		military_raio_zealot = len(self.units(ZEALOT)) / 10
		if military_raio_zealot > 1.0:
			military_raio_zealot = 1

		military_raio_immortal = len(self.units(IMMORTAL)) / 10
		if military_raio_immortal > 1.0:
			military_raio_immortal = 1


		cv2.line(game_data, (0, 35), (int(line_max*military_raio_adept), 35), (215, 175, 55), 2)
		cv2.line(game_data, (0, 31), (int(line_max*military_raio_zealot), 31), (10, 10, 215), 2)
		cv2.line(game_data, (0, 27), (int(line_max*military_raio_immortal), 27), (55, 175, 215), 2)
		cv2.line(game_data, (0, 23), (int(line_max*military_raio_stalker), 23), (40, 210, 100), 2)
		cv2.line(game_data, (0, 19), (int(line_max*military_raio_voidray), 19), (30, 255, 150), 2)
		cv2.line(game_data, (0, 15), (int(line_max*plausible_supply), 15), (0, 50, 250), 2)
		cv2.line(game_data, (0, 11), (int(line_max*population_ratio), 11), (250, 50, 150), 2)
		cv2.line(game_data, (0, 7), (int(line_max*vaspene_ratio), 7), (250, 50, 250), 2)
		cv2.line(game_data, (0, 3), (int(line_max*mineral_ratio), 3), (250, 250, 0), 2)
		

		self.flip = cv2.flip(game_data, 0)
		resized = cv2.resize(self.flip, dsize = None, fx = 3, fy = 3)
		cv2.imshow('Intel', resized)
		cv2.waitKey(1)


	async def build_workers(self):
		if (len(self.units(NEXUS)) * 16) > len(self.units(PROBE)) and len(self.units(PROBE)) < self.MAX_WORKERS:
			if len(self.units(PROBE)) < self.MAX_WORKERS:
				for nexus in self.units(NEXUS).ready.noqueue:
					if self.can_afford(PROBE):
						await self.do(nexus.train(PROBE))

	async def build_pylons(self):
		if self.supply_left < 5 and not self.already_pending(PYLON):
			nexuses = self.units(NEXUS).ready
			if nexuses.exists:
				if self.can_afford(PYLON):
					await self.build(PYLON, near=nexuses.first)

	async def build_assimilators(self):
		for nexus in self.units(NEXUS).ready:
			vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
			for vaspene in vaspenes:
				workers = self.select_build_worker(vaspene.position)
				if not self.can_afford(ASSIMILATOR):
					break
				if workers is None:
					break
				if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
					await self.do(workers.build(ASSIMILATOR, vaspene))

	async def expand(self):
		if self.units(NEXUS).amount < (self.iteration / self.ITERATION_PER_MINUTE) and self.can_afford(NEXUS):
			await self.expand_now()

	async def buildings_offensive(self):
		#print(self.iteration / self.ITERATION_PER_MINUTE)
		if self.units(PYLON).ready.exists:
			pylon = self.units(PYLON).ready.random

			if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
				if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
					await self.build(CYBERNETICSCORE, near=pylon)

			elif len(self.units(GATEWAY)) < 1:
				if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
					await self.build(GATEWAY, near=pylon)

			if self.units(CYBERNETICSCORE).ready.exists:
				if len(self.units(ROBOTICSFACILITY)) < 1:
					if self.can_afford(ROBOTICSFACILITY) and not self.already_pending(ROBOTICSFACILITY):
						await self.build(ROBOTICSFACILITY, near=pylon)

			if self.units(CYBERNETICSCORE).ready.exists:
				if len(self.units(STARGATE)) < (self.iteration / self.ITERATION_PER_MINUTE):
					if self.can_afford(STARGATE) and not self.already_pending(STARGATE):
						await self.build(STARGATE, near=pylon)


	async def forces(self):
		for sg in self.units(STARGATE).ready.noqueue:
			if self.can_afford(VOIDRAY) and self.supply_left > 0:
				await self.do(sg.train(VOIDRAY))

	async def forces2(self):
		for gw in self.units(GATEWAY).ready.noqueue:
			if self.units(VOIDRAY).amount > 1:
				if self.can_afford(STALKER) and self.supply_left > 0:
					await self.do(gw.train(STALKER))

	async def forces3(self):
		gateways = self.units(GATEWAY).ready.noqueue
		if gateways.exists and self.units(STALKER).amount > 1:
			if self.can_afford(ZEALOT):
				await self.do(random.choice(gateways).train(ZEALOT))

	async def forces4(self):
		for gw in self.units(GATEWAY).ready.noqueue:
			if self.units(CYBERNETICSCORE).exists and self.units(ZEALOT).amount > 0:
				if self.can_afford(ADEPT) and self.supply_left > 0:
					await self.do(gw.train(ADEPT))

	async def forces5(self):
		for rf in self.units(ROBOTICSFACILITY).ready.noqueue:
			if self.can_afford(IMMORTAL) and self.supply_left > 0:
				await self.do(rf.train(IMMORTAL))


	def find_target(self, state):
		if len(self.known_enemy_units) > 0:
			return random.choice(self.known_enemy_units)
		elif len(self.known_enemy_structures) > 0:
			return random.choice(self.known_enemy_structures)
		else:
			return self.enemy_start_locations[0]

	'''async def morph_gateway(self):
		for gateway in self.units(GATEWAY).ready:
			abilities = await self.get_available_abilities(gateway)
			if AbilityId.MORPH_WARPGATE in abilities and self.can_afford(AbilityId.MORPH_WARPGATE):
				await self.do(gateway(MORPH_WARPGATE))'''


	async def attack(self):
		#aggressive_worker = {STALKER: [15, 3], VOIDRAY: [8, 3]}
		'''
		aggressive_worker = {VOIDRAY: [8, 3]}
		for UNIT in aggressive_worker:
			if self.units(UNIT).amount > aggressive_worker[UNIT][0] and self.units(UNIT).amount > aggressive_worker[UNIT][1]:
				for s in self.units(UNIT).idle:
					await self.do(s.attack(self.find_target(self.state)))

			elif self.units(UNIT).amount > aggressive_worker[UNIT][1]:
				if len(self.known_enemy_units) > 0:
					for s in self.units(UNIT).idle:
						await self.do(s.attack(random.choice(self.known_enemy_units)))'''
		if len(self.units(VOIDRAY).idle) > 0:
			choice = random.randrange(0, 8)
			target = False
			if self.iteration > self.do_something_after:
				if choice == 0:
					wait = random.randrange(20, 165)
					self.do_something_after = self.iteration + wait

				elif choice == 1:
					if len(self.known_enemy_units) > 0:
						target = self.known_enemy_units.closest_to(random.choice(self.units(NEXUS)))

				elif choice == 2:
					if len(self.known_enemy_structures) > 0:
						target = random.choice(self.known_enemy_structures)

				elif choice == 3:
					target = self.enemy_start_locations[0]

				elif choice == 4:
					if len(self.known_enemy_units) > 0:
						for gw in self.units(STALKER).idle:
							tar = self.known_enemy_units.closest_to(random.choice(self.units(NEXUS)))
							await self.do(gw.attack(tar))

				elif choice == 5:
					if len(self.known_enemy_structures) > 0:
						for im in self.units(IMMORTAL).idle:
							tar = self.enemy_start_locations[0]
							await self.do(im.attack(tar))

				elif choice == 6:
					if len(self.known_enemy_units) > 0:
						for ze in self.units(ADEPT).idle:
							tar = self.known_enemy_units.closest_to(random.choice(self.units(NEXUS)))
							await self.do(ze.attack(tar))

				elif choice == 7:
					if len(self.known_enemy_units) > 0:
						for ze in self.units(ZEALOT).idle:
							tar = self.known_enemy_units.closest_to(random.choice(self.units(NEXUS)))
							await self.do(ze.attack(tar))

				if target:
					for vr in self.units(VOIDRAY).idle:
						await self.do(vr.attack(target))

				y = np.zeros(8)
				y[choice] = 1
				print(y)
				self.train_data.append([y, self.flip])
			#print(len(self.train_data))


number_of_games = input("How many simulated runs:")
for i in range(int(number_of_games)):
	run_game(maps.get("PortAleksanderLE"), [Bot(Race.Protoss, AIbot()), Computer(Race.Protoss, Difficulty.Easy)], realtime = False)
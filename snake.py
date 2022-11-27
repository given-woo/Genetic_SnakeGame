import math

import pygame
import os, random
import numpy as np

FPS=60
SCREEN_SIZE = 10
PIXEL_SIZE = 30
LINE_WIDTH = 1

DIRECTIONS = np.array([
    (0, -1),  # UP
    (1, 0),  # RIGHT
    (0, 1),  # DOWN
    (-1, 0),  # LEFT
])


class Snake():
    snake, fruit = None, None

    def __init__(self, s, genome):
        self.genome = genome

        self.s = s
        self.score = 0
        self.snake = np.array([[5, 6], [5, 7], [5, 8], [5, 9]])
        self.direction = 0  # UP
        self.place_fruit()
        self.timer = 0
        self.last_fruit_time = 0
        self.count=0

        # fitness
        self.fitness = 0.
        self.last_dist = np.inf

    def place_fruit(self, coord=None):
        if coord:
            self.fruit = np.array(coord)
            return

        while True:
            x = random.randint(0, SCREEN_SIZE - 1)
            y = random.randint(0, SCREEN_SIZE - 1)
            if list([x, y]) not in self.snake.tolist():
                break
        self.fruit = np.array([x, y])

    def step(self, direction):
        self.count+=1
        old_head = self.snake[0]
        movement = DIRECTIONS[direction]
        new_head = old_head + movement

        if (
                new_head[0] < 0 or
                new_head[0] >= SCREEN_SIZE or
                new_head[1] < 0 or
                new_head[1] >= SCREEN_SIZE or
                new_head.tolist() in self.snake.tolist()
        ):
            self.fitness = self.count + math.pow(2, self.score) + 500 * math.pow(self.score, 2.1) - 0.25 * math.pow(self.count, 1.3) * math.pow(self.score, 1.2)
            return False

        # eat fruit
        if all(new_head == self.fruit):
            self.last_fruit_time = self.timer
            self.score += 1
            self.place_fruit()
        else:
            tail = self.snake[-1]
            self.snake = self.snake[:-1, :]

        self.snake = np.concatenate([[new_head], self.snake], axis=0)
        return True

    def get_inputs(self):
        head = self.snake[0]
        result = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
        four_dirs = [
            DIRECTIONS[self.direction],  # straight forward
            DIRECTIONS[(self.direction + 3) % 4],  # left
            DIRECTIONS[(self.direction + 1) % 4],  # right
            DIRECTIONS[(self.direction + 2) % 2],  # back
        ]

        # check for walls
        for i, p_dir in enumerate(four_dirs):
            for j in range(10):
                guess_head = head + p_dir * (j + 1)
                if (
                        guess_head[0] < 0 or
                        guess_head[0] >= SCREEN_SIZE or
                        guess_head[1] < 0 or
                        guess_head[1] >= SCREEN_SIZE
                ):
                    result[i] = j * 0.1
                    break
        for i in range(3):
            for j in range(10):
                guess_head = head + four_dirs[i%3]+four_dirs[(i+1)%3] * (j + 1)
                if (
                        guess_head[0] < 0 or
                        guess_head[0] >= SCREEN_SIZE or
                        guess_head[1] < 0 or
                        guess_head[1] >= SCREEN_SIZE
                ):
                    result[4+i] = j * 0.1
                    break

        # check for tail
        for i, p_dir in enumerate(four_dirs):
            for j in range(10):
                guess_head = head + p_dir * (j + 1)
                if guess_head.tolist() in self.snake.tolist():
                    result[8+i] = j * 0.1
                    break
        for i in range(3):
            for j in range(10):
                guess_head = head + four_dirs[i%3]+four_dirs[(i+1)%3] * (j + 1)
                if guess_head.tolist() in self.snake.tolist():
                    result[12+i] = j * 0.1
                    break

        # check for fruit
        for i, p_dir in enumerate(four_dirs):
            for j in range(10):
                guess_head = head + p_dir * (j + 1)
                if all(guess_head == self.fruit):
                    result[16+i] = j * 0.1
                    break
        for i in range(3):
            for j in range(10):
                guess_head = head + four_dirs[i%3]+four_dirs[(i+1)%3] * (j + 1)
                if all(guess_head == self.fruit):
                    result[20+i] = j * 0.1
                    break
        
        #print(result)
        return np.array(result)

    def run(self):
        self.fitness = 0

        prev_key = pygame.K_UP

        font = pygame.font.SysFont(None, 20)
        font.set_bold(True)
        appleimage = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        appleimage.fill((0, 255, 0))
        img = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        img.fill((255, 0, 0))
        clock = pygame.time.Clock()

        while True:
            self.timer += 0.1
            if self.timer - self.last_fruit_time > 0.1 * FPS * 2:
                break

            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:
                    # QUIT
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    # PAUSE
                    if e.key == pygame.K_SPACE:
                        pause = True
                        while pause:
                            for ee in pygame.event.get():
                                if ee.type == pygame.QUIT:
                                    pygame.quit()
                                elif ee.type == pygame.KEYDOWN:
                                    if ee.key == pygame.K_SPACE:
                                        pause = False
                    if __name__ == '__main__':
                        # CONTROLLER
                        if prev_key != pygame.K_DOWN and e.key == pygame.K_UP:
                            self.direction = 0
                            prev_key = e.key
                        elif prev_key != pygame.K_LEFT and e.key == pygame.K_RIGHT:
                            self.direction = 1
                            prev_key = e.key
                        elif prev_key != pygame.K_UP and e.key == pygame.K_DOWN:
                            self.direction = 2
                            prev_key = e.key
                        elif prev_key != pygame.K_RIGHT and e.key == pygame.K_LEFT:
                            self.direction = 3
                            prev_key = e.key

            # action
            if __name__ != '__main__':
                inputs = self.get_inputs()
                outputs = self.genome.forward(inputs)
                outputs = np.argmax(outputs)

                if outputs == 0:  # straight
                    pass
                elif outputs == 1:  # left
                    self.direction = (self.direction + 3) % 4
                elif outputs == 2:  # right
                    self.direction = (self.direction + 1) % 4

            if not self.step(self.direction):
                break

            self.s.fill((0, 0, 0))
            pygame.draw.rect(self.s, (255, 255, 255), [0, 0, SCREEN_SIZE * PIXEL_SIZE, LINE_WIDTH])
            pygame.draw.rect(self.s, (255, 255, 255),
                             [0, SCREEN_SIZE * PIXEL_SIZE - LINE_WIDTH, SCREEN_SIZE * PIXEL_SIZE, LINE_WIDTH])
            pygame.draw.rect(self.s, (255, 255, 255), [0, 0, LINE_WIDTH, SCREEN_SIZE * PIXEL_SIZE])
            pygame.draw.rect(self.s, (255, 255, 255), [SCREEN_SIZE * PIXEL_SIZE - LINE_WIDTH, 0, LINE_WIDTH,
                                                       SCREEN_SIZE * PIXEL_SIZE + LINE_WIDTH])
            for bit in self.snake:
                self.s.blit(img, (bit[0] * PIXEL_SIZE, bit[1] * PIXEL_SIZE))
            self.s.blit(appleimage, (self.fruit[0] * PIXEL_SIZE, self.fruit[1] * PIXEL_SIZE))
            score_ts = font.render(str(self.score)+" Points", False, (255, 255, 255))
            self.s.blit(score_ts, (5, 5))
            pygame.display.update()

        return self.fitness, self.score


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
    pygame.display.set_caption('Snake')

    while True:
        snake = Snake(s, genome=None)
        fitness, score = snake.run()

        print('Fitness: %s, Score: %s' % (fitness, score))
# Just a demo for now :-)

import pygame
import rabbyt

class Piece(rabbyt.Sprite):
    def __init__(self, **kargs):
        rabbyt.Sprite.__init__(self, **kargs)

size = (800, 600)

pygame.init()
pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
rabbyt.set_viewport(size, projection=(0, 0, 800, 600))
rabbyt.set_default_attribs()

pieces = [Piece(xy=attributes[0], texture=attributes[1]) for attributes in
        [((100, 100), 'red_viking.png'),
         ((200, 50),  'green_viking.png'),
         ((300, 150), 'island_tile.png'),
         ((400, 100), 'island_tile.png')]]
grabbed_point = None

print "Click and drag the pieces. Scrollwheel to rotate pieces."

clock = pygame.time.Clock()
running=True
z=0
offset_x = 0
offset_y = 0
while running:
    clock.tick(40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
        	    z += 10
        	    rabbyt.set_viewport(size, projection=(z,z,800-z,600-z))
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grabbed_point = None
            # sort based on z-order
            collisions = sorted(rabbyt.collisions.collide_single((event.pos[0], event.pos[1]), pieces), cmp=lambda x, y: cmp(pieces.index(y), pieces.index(x)))
            
            if collisions:
                grabbed_point = collisions[0]
            
            if grabbed_point:
                pieces.remove(grabbed_point)
                pieces.append(grabbed_point)
                grabbed_point.rgb = (.5, .5, .5)
                #grabbed_point.scale = rabbyt.lerp(1, 1.25, dt=100, extend="reverse")
            
            if event.button == 4 and grabbed_point:
                grabbed_point.rot += 15
            elif event.button == 5 and grabbed_point:
                grabbed_point.rot -= 15
            else:
                if grabbed_point:
                    offset_x = grabbed_point.x-event.pos[0]
                    offset_y = grabbed_point.y-event.pos[1]
        elif event.type == pygame.MOUSEMOTION:
            
            if grabbed_point:
                grabbed_point.x = event.pos[0] + offset_x
                grabbed_point.y = event.pos[1] + offset_y
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if grabbed_point:
                grabbed_point.rgb = (1, 1, 1)
                # grabbed_point.scale = rabbyt.lerp(1.25, 1, dt=200)
            grabbed_point = None

    rabbyt.set_time(pygame.time.get_ticks())
    rabbyt.clear()
    rabbyt.render_unsorted(pieces)
    pygame.display.flip()

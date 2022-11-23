import math
import numpy as np

class gridCoord(object):
    
    def __init__(self, x=0, y=0, *coords):
        self._x = None;
        self._y = None;
        if coords and (type(coords[0]) != int or type(coords[0]) != float):
            self.x = coords[0][0]
            self.y = coords[0][1]
        elif coords and (type(coords[0]) == gridCoord):
            self.x = coords[0].x
            self.y = coords[0].y
        elif coords:
            self.x = coords[0]
            self.y = coords[1]
        else:
            self.x = x
            self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val
   
    def distance(self, coord):
       return math.sqrt( (coord.x - self.x)**2 + (coord.y-self.y)**2)

    def __getitem__(self, key):
        return [self._x,self._y][key]

    def __setitem__(self, key, val):
        if key == 0:
            self._x = val
        elif key == 1:
            self._y = val

    def __add__(self, val):
        if type(val) == gridCoord or type(val) == list or type(val) == tuple:
            return gridCoord(x=self.x+val[0], y=self.y+val[1])
        elif type(val) == int or type(val) == float:
            return gridCoord(x=self.x+val, y=self.y+val)

    def __sub__(self, val):
        if type(val) == gridCoord or type(val) == list or type(val) == tuple:
            return gridCoord(x=self.x-val[0], y=self.y-val[1])
        elif type(val) == int or type(val) == float:
            return gridCoord(x=self.x-val, y=self.y-val)

    def __truediv__(self, val):
        if type(val) == int or type(val) == float:
            return gridCoord(x=self.x/val, y=self.y/val)
    
    def __floordiv__(self, val):
        if type(val) == int or type(val) == float:
            return gridCoord(x=self.x//val, y=self.y//val)

    def toList(self):
        return [self.x, self.y]

    def angleTo(self, coord):
        return (math.degrees(math.atan2(coord.x - self.x, coord.y - self.y))) % 360


class Boid(object):
    boids = []

    @staticmethod
    def step():
        for boid in Boid.boids:
            boid.step()
    
    @property
    def pos(self):
        return self._position

    @pos.setter
    def pos(self, val):
        self._position = gridCoord(val)

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, val):
        self._position[0] = val

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, val):
        self._position[1] = val

    @property
    def vector(self):
        return self._vector
    
    @vector.setter
    def vector(self, val):
        self._vector = val

    def __init__(self, name, x=0, y=0,vector=np.array([0,0]),speed=0.1,range=100):
        self._speed = speed
        self._position = gridCoord(x,y)
        self._range = range
        self._vector = vector
        self.name = name
        self.sep_weight = 1
        self.coh_weight = 1
        self.ali_weight = 1
        Boid.boids.append(self)

    """def __del__(self):
        Boid.boids.remove(self)"""
    
    def step(self, time=0.1):
        # move the boid forward by the sum vector (speed by direction)
        move_dir = self.separation() * self.sep_weight
        move_dir += self.alignment() * self.ali_weight
        move_dir += self.cohesion()  * self.coh_weight
        self._vector = self._normalize(self._vector + (move_dir / 3))
        for i in range(2):
            self._position[i] += self._vector[i] * self._speed * time

    def avoid_walls(self, walls):
        # check if any wall intercepts vision, if so apply a turning vector towards the normal ... I think 
        pass

    def separation(self):
        # for this each boid in local vision will give a weight for direction they should steer away from, the closer the stronger the weight
        weight_dir_sum = np.array([0,0], dtype=np.dtype('float64'))
        weight_sum = 0
        for boid in self._get_local_boids():
            # calculate the angle to boid
            v = self._normalize(np.array(boid.pos.toList()) - np.array(self.pos.toList()))
            # calc the weight of it 
            w = math.sqrt(((self.pos.distance(boid.pos)-self._range)/self._range)**2)
            weight_dir_sum = weight_dir_sum + (v * w)
            weight_sum += w
        if weight_sum == 0:
            return 0
        return self._normalize(weight_dir_sum / weight_sum) * -1
    
    def cohesion(self):
        pos_sum = gridCoord()
        counter = 0
        for boid in self._get_local_boids():
            pos_sum += boid.pos
            counter += 1
        if counter == 0:
            return 0
        return  self._normalize(np.array(((pos_sum / counter) - self.pos).toList()))

    def alignment(self):
        # average the vectors
        vectors_sum = np.array([0,0], dtype='float64')
        counter = 0
        for boid in self._get_local_boids():
            vectors_sum += boid.vector
            counter = 0
        if counter == 0:
            return 0
        return self._normalize(vectors_sum / counter)

    
    @staticmethod
    def _normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0: 
            return v
        return v / norm

    def _get_local_boids(self):
        boids = []
        for boid in Boid.boids:
            if (boid != self) and (self.pos.distance(boid.pos) <= self._range):
                # boid is in range 
                boids.append(boid)
        return boids

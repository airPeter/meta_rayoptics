import numpy as np
import matplotlib.pyplot as plt

class Ray:
    def __init__(self, y, theta):
        self.y = y
        self.theta = theta
        if self.y.size != self.theta.size:
            raise Exception("the size of y and theta must equal.")
    def __len__(self,):
        return self.y.size

class OpticalPath:
    def __init__(self):
        self.elements = []
        self.rays = []
        self.N = None
        self.p = None
        
    def add(self,ele):
        self.elements.append(ele)
    
    def run(self, ray):
        self.N = len(ray)
        self.rays.append(ray)
        self.p = np.ones((self.N, ), dtype= np.bool)
        tmp_ray = ray
        for ele in self.elements:
            tmp_ray = ele(tmp_ray)
            self.rays.append(tmp_ray)
        return tmp_ray
    
    def vis_path(self, y_lim = None):
        x_plot = [0]
        y_plot = [self.rays[0].y]
        plt.figure()
        for i, ele in enumerate(self.elements):
            if hasattr(ele, 'p'):
                # if ele.p dones't work, becase, The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
                if not (ele.p is None):
                    self.p = self.p & ele.p

            if ele.d != 0:
                x_plot.append(x_plot[-1] + ele.d)
                y_plot.append(self.rays[i + 1].y)

            if hasattr(ele, 'r'):
                plt.vlines(x = x_plot[-1], ymax= ele.r, ymin = -ele.r, linewidth = 4, colors = 'k', alpha = 0.5)
            if hasattr(ele, 'f'):
                #plt.axvline(x = x_plot[-1], linestyle = '--', c = 'gray')
                plt.axvline(x = x_plot[-1] + ele.f, linestyle = '--', c = 'gray')
        y_plot = np.array(y_plot)
        for i in range(self.N):
            if self.p[i]:
                _ = plt.plot(x_plot, y_plot[:, i], c = 'b')
        plt.xlabel('distance')
        if y_lim:
            plt.ylim(y_lim)
        plt.show()
        return None    

class meta_lens:
    def __init__(self, f, r = None):
        self.f = f
        self.d = 0
        if r:
            self.pupil = pupil(r)
            self.r = r
        else:
            self.pupil = None
        self.p = None
        
    def __call__(self, ray):
        if self.pupil:
            ray = self.pupil(ray)
            self.p = self.pupil.p
        y = ray.y.copy()
        theta = ray.theta.copy()
        dphi_dx = - y / np.sqrt(y**2 + self.f**2)
        theta = np.arcsin(np.sin(theta) + dphi_dx)
        # #if the ray angle is too large, not will not be ploted.
        # p_theta = np.abs(theta) < np.pi/3
        # if self.p is None:
        #     self.p = p_theta
        # else:
        #     self.p = self.p & p_theta
        return Ray(y, theta)

class pupil:
    def __init__(self, r):
        self.p = None
        self.r = r
        
    def __call__(self, ray):
        y = ray.y.copy()
        self.p = (self.r - np.abs(y) > 0)
        return ray
        
class freespace:
    def __init__(self, d):
        self.d = d
    def __call__(self, ray):
        y = ray.y.copy()
        theta = ray.theta.copy()
        y += self.d * np.tan(theta)
        return Ray(y, theta)
     
import numpy as np
from mayavi import mlab


class visScan():
    def __init__(self):
        self.fig = None
    def read_bin(self, path):
        pointcloud = np.fromfile(path, dtype=np.float32).reshape(-1, 4)
        x = pointcloud[:, 0]
        y = pointcloud[:, 1] / 20.0
        z = pointcloud[:, 2] / 20.0
        i = pointcloud[:, 3]
        vals = 'height'
        if vals == "height":
            col = z
        else:
            col = i
        return x, y, z, col

    def show(self, file_path):
        x = None
        y = None
        z = None
        col = None
        x, y, z, col = self.read_bin(file_path)
        if self.fig is None:
            self.fig = mlab.figure(bgcolor=(0.136, 0.329, 0.222), size=(640, 500))
            # self.fig = mlab.figure(size=(640, 500))

        else:
            self.fig = mlab.figure(figure=self.fig, bgcolor=(0.136, 0.329, 0.222) )
            # self.fig = mlab.figure(figure=self.fig)

        l = mlab.points3d(x, y, z,
                             col,  # Values used for Color
                             mode="point",
                             # 灰度图的伪彩映射
                             colormap='spectral',  # 'bone', 'copper', 'gnuplot'
                             # color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                             figure=self.fig,
                             )
        # 绘制原点
        mlab.points3d(0, 0, 0, color=(1, 1, 1), mode="sphere", scale_factor=0.2)
        # 绘制坐标
        axes = np.array(
            [[20.0, 0.0, 0.0, 0.0], [0.0, 20.0, 0.0, 0.0], [0.0, 0.0, 34.0, 0.0]],
            dtype=np.float64,
        )
        #x轴
        mlab.plot3d(
            [0, axes[0, 0]],
            [0, axes[0, 1]],
            [0, axes[0, 2]],
            color=(1, 0, 0),
            tube_radius=None,
            figure=self.fig,
        )
        #y轴
        mlab.plot3d(
            [0, axes[1, 0]],
            [0, axes[1, 1]],
            [0, axes[1, 2]],
            color=(0, 1, 0),
            tube_radius=None,
            figure=self.fig,
        )
        #z轴
        mlab.plot3d(
            [0, axes[2, 0]],
            [0, axes[2, 1]],
            [0, axes[2, 2]],
            color=(0, 0, 1),
            tube_radius=None,
            figure=self.fig,
        )
        # l.mlab_source.reset(x=x, y=y, z=z, col=col)
        mlab.show(func=None, stop=False)


    def read_bin2(self, path):
        pointcloud = np.fromfile(path, dtype=np.float32).reshape(-1, 4)
        x = pointcloud[:, 0]
        y = pointcloud[:, 1]
        z = pointcloud[:, 2]
        i = pointcloud[:, 3]
        vals = 'height'
        if vals == "height":
            col = z
        else:
            col = i
        return x, y, z, col

    def show2(self, file_path):
        x = None
        y = None
        z = None
        col = None
        x, y, z, col = self.read_bin2(file_path)
        if self.fig is None:
            self.fig = mlab.figure(bgcolor=(0.136, 0.329, 0.222), size=(640, 500))
        else:
            self.fig = mlab.figure(figure=self.fig)
        l = mlab.points3d(x, y, z,
                             col,  # Values used for Color
                             mode="point",
                             # 灰度图的伪彩映射
                             colormap='spectral',  # 'bone', 'copper', 'gnuplot'
                             # color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                             figure=self.fig,
                             )
        # 绘制原点
        mlab.points3d(0, 0, 0, color=(1, 1, 1), mode="sphere", scale_factor=0.2)
        # 绘制坐标
        axes = np.array(
            [[20.0, 0.0, 0.0, 0.0], [0.0, 20.0, 0.0, 0.0], [0.0, 0.0, 20.0, 0.0]],
            dtype=np.float64,
        )
        #x轴
        mlab.plot3d(
            [0, axes[0, 0]],
            [0, axes[0, 1]],
            [0, axes[0, 2]],
            color=(1, 0, 0),
            tube_radius=None,
            figure=self.fig,
        )
        #y轴
        mlab.plot3d(
            [0, axes[1, 0]],
            [0, axes[1, 1]],
            [0, axes[1, 2]],
            color=(0, 1, 0),
            tube_radius=None,
            figure=self.fig,
        )
        #z轴
        mlab.plot3d(
            [0, axes[2, 0]],
            [0, axes[2, 1]],
            [0, axes[2, 2]],
            color=(0, 0, 1),
            tube_radius=None,
            figure=self.fig,
        )
        # l.mlab_source.reset(x=x, y=y, z=z, col=col)
        mlab.show(func=None, stop=False)

    def close(self):
        if self.fig is not None:
            mlab.clf(self.fig)
            # self.fig = None



import numpy as np
from dagline import WorkerNode
from ZebVR.utils import get_time_ns, append_timestamp_to_filename

class HeadEmbeddedSaver(WorkerNode):

    def __init__(
            self,
            filename: str = 'head_embedded_data.csv',
            num_tail_points_interp: int = 20,
            *args,
            **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.num_tail_points_interp = num_tail_points_interp
        self.fs = None

    def set_filename(self, filename: str):
        self.filename = filename
    
    def initialize(self):
        super().initialize()

        file = append_timestamp_to_filename(self.filename)


        self.fd = open(file, 'w')
        headers = (
            'index',
            'timestamp',
            'identity',
            'latency_ms',
            'est_x',
            'est_y',
            'pc1_x',
            'pc1_y',
            'pc2_x',
            'pc2_y',
            'est_theta',
            'strength',
            'turning_strength',
            'v_feedback_now_pix',
            'omega_feedback_now_rad',
        ) \
        + tuple(f"tail_point_{n:03d}_x" for n in range(self.num_tail_points_interp)) \
        + tuple(f"tail_point_{n:03d}_y" for n in range(self.num_tail_points_interp))
        self.fd.write(','.join(headers) + '\n')

    
    def cleanup(self):
        super().cleanup()
        if self.fd is not None:
            self.fd.close()

    def process_data(self, data):
        
        if self.fd is None:
            return
        
        if data is None:
            return

        fish_centroid = np.zeros((2,), dtype=float)
        fish_caudorostral_axis = np.zeros((2,), dtype=float)
        fish_mediolateral_axis = np.zeros((2,), dtype=float)
        # skeleton_interp = np.zeros((self.num_tail_points_interp,2), dtype=float)

        try:

            fish_centroid[:] = data['tracking']['body']['centroid_global']
            body_axes = data['tracking']['body']['body_axes_global']
            fish_caudorostral_axis[:] = body_axes[:,0]
            fish_mediolateral_axis[:] = body_axes[:,1] 
            

        except KeyError as err:
            print(f'KeyError: {err}')
            return None 
        
        except TypeError as err:
            print(f'TypeError: {err}')
            return None
        
        except ValueError as err:
            print(f'ValueError: {err}')
            return None

        latency = 1e-6*(get_time_ns() - data['timestamp'])
        #print(f"frame {data['index']}, fish {data['identity']}: latency {latency}")

        row = (
            f"{data['index']}",
            f"{data['timestamp']}",
            f"{data['identity']}",
            f"{latency}",
            f"{fish_centroid[0]}",
            f"{fish_centroid[1]}",
            f"{fish_caudorostral_axis[0]}",
            f"{fish_caudorostral_axis[1]}",
            f"{fish_mediolateral_axis[0]}",
            f"{fish_mediolateral_axis[1]}",
            f"{left_eye_centroid[0]}",
            f"{left_eye_centroid[1]}",
            f"{left_eye_angle}",
            f"{right_eye_centroid[0]}",
            f"{right_eye_centroid[1]}",
            f"{right_eye_angle}",
        ) \
        + tuple(f"{skeleton_interp[i,0]}" for i in range(self.num_tail_points_interp)) \
        + tuple(f"{skeleton_interp[i,1]}" for i in range(self.num_tail_points_interp)) 

        self.fd.write(','.join(row) + '\n')

        res = {
            'frame': data['index'],
            'fish_id': data['identity'],
            'latency': latency
        }
        return res
        
    def process_metadata(self, metadata) -> None:
        pass

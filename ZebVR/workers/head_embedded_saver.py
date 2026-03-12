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
        
        if data in None:
            return
        
        # FILL VALUES IN HERE

    # except KeyError as err:
    #     print(f'KeyError: {err}')
    #     return None 
    
    # except TypeError as err:
    #     print(f'TypeError: {err}')
    #     return None
    
    # except ValueError as err:
    #     print(f'ValueError: {err}')
    #     return None
        latency = 1e-6*(get_time_ns() - data['timestamp'])

        # WRITE ROW HERE



    def process_metadata(self, metadata) -> None:
        pass

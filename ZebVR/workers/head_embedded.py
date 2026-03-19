"""
TO BE MOVED TO OTHER REPO
"""
from typing import Any, Dict
from dagline import WorkerNode
import numpy as np
from numpy.typing import NDArray

ENABLE_KALMAN = False

from head_embedded import HeadEmbeddedState, SingleFishHeadEmbedded

class HeadEmbeddedWorker(WorkerNode):

    def __init__(
            self,
            head_embedded: SingleFishHeadEmbedded = SingleFishHeadEmbedded(),
            state: HeadEmbeddedState = HeadEmbeddedState(),
            *args,
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.head_embedded = head_embedded
        self.state = state
        # self.cropped = cropped  
        self.current_estimator = None

    def process_data(self, data: NDArray) -> Dict:
        if data is None:
            return None
        try:
            fields = data['tracking'].dtype.names
            print(fields)
            head_embedded, self.state = self.head_embedded.process(data['tracking']['tail']['image_processed'], self.state)
        except KeyError as err:
            print(f'KeyError: {err}')
            return None 
        
        except TypeError as err:
            print(f'TypeError: {err}')
            return None
        
        except ValueError as err:
            print(f'ValueError -2: {err}')
            return None
        msg = np.array(
            (data['index'], data['timestamp'], head_embedded, data['origin'], data['shape'], data['identity']),
            dtype=np.dtype([
                ('index', int),
                ('timestamp', np.int64),
                ('tracking', head_embedded.dtype),
                ('origin', np.int32, (2,)),
                ('shape', np.int32, (2,)),
                ('identity', np.int32),
            ])
        )

        res = {}
        res['head_embedded_output_stim'] = msg 
        res['head_embedded_output_saver'] = msg 
   
        return res
    

    def process_metadata(self, meta_data) -> Any:
        pass



        


        

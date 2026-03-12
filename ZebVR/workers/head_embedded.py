"""
TO BE MOVED TO OTHER REPO
"""
from typing import Any, Dict
from dagline import WorkerNode
import numpy as np
from numpy.typing import NDArray

ENABLE_KALMAN = False

from head_embedded.core import HeadEmbeddedState
from head_embedded.single_fish.single_fish_head_embedded import SingleFishHeadEmbedded

class HeadEmbeddedWorker(WorkerNode):

    def __init__(
            self,
            fish_vr: SingleFishHeadEmbedded = SingleFishHeadEmbedded(),
            state: HeadEmbeddedState = HeadEmbeddedState(),
            *args,
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.fish_vr = fish_vr
        self.state = state
        # self.cropped = cropped  
        self.current_estimator = None

    def process_data(self, data: NDArray) -> Dict:

        if data is None:
            return None
        
        self.state = self.fish_vr.process(data['image'], self.state)

        msg = np.array(
            (data['index'], data['timestamp'], estimator, data['origin'], data['shape'], data['identity']),
            dtype=np.dtype([
                ('index', int),
                ('timestamp', np.int64),
                ('tracking', estimator.dtype),
                ('origin', np.int32, (2,)),
                ('shape', np.int32, (2,)),
                ('identity', np.int32),
            ])
        )

        res = {}
        res['estimator'] = msg
        # todo change visual according to estimator 
        return res
    

    def process_meta_data(self, meta_data) -> Any:
        pass



        


        

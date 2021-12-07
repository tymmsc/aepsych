#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import warnings
from typing import Optional, Union

import numpy as np
import torch
from aepsych.config import Config
from aepsych.generators.base import AEPsychGenerator
from aepsych.utils import _process_bounds
from aepsych.models.base import AEPsychMixin


class RandomGenerator(AEPsychGenerator):
    """Generator that generates points randomly without an acquisition function."""

    def __init__(
        self,
        lb: Union[np.ndarray, torch.Tensor],
        ub: Union[np.ndarray, torch.Tensor],
        dim: Optional[int] = None,
    ):
        """Iniatialize RandomGenerator.
        Args:
            lb (Union[np.ndarray, torch.Tensor]): Lower bounds of each parameter.
            ub (Union[np.ndarray, torch.Tensor]): Upper bounds of each parameter.
            dim (int, optional): Dimensionality of the parameter space. If None, it is inferred from lb and ub.
        """

        self.lb, self.ub, self.dim = _process_bounds(lb, ub, dim)
        self.bounds_ = torch.stack([self.lb, self.ub])

    def gen(
        self,
        num_points: int = 1,  # Current implementation only generates 1 point at a time
        model: AEPsychMixin = None,  # included for API compatibility.
    ) -> np.ndarray:
        """Query next point(s) to run by randomly sampling the parameter space.
        Args:
            num_points (int, optional): Number of points to query. Currently, only 1 point can be queried at a time.
        Returns:
            np.ndarray: Next set of point(s) to evaluate, [num_points x dim].
        """
        if num_points != 1:
            warnings.warn("RandomGenerator currently only generates 1 point at a time.")
        X = self.bounds_[0] + torch.rand(self.bounds_.shape[1]) * (
            self.bounds_[1] - self.bounds_[0]
        )
        return X.unsqueeze(0).numpy()

    @classmethod
    def from_config(cls, config: Config):
        return cls()
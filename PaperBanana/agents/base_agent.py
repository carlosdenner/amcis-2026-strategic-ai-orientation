# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Base class for agents
"""

import re
from typing import List, Dict, Any
from abc import ABC, abstractmethod

import json_repair

from utils.config import ExpConfig


class BaseAgent(ABC):
    """Base class for agents"""

    def __init__(
        self,
        model_name: str = "",
        system_prompt: str = "",
        exp_config: "ExpConfig" = None,
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.exp_config = exp_config

    async def call_text_model(
        self, contents, temperature=None, candidate_count=1,
        max_output_tokens=50000, max_attempts=5, retry_delay=5,
    ):
        """Dispatch text generation to the correct backend based on model name."""
        from utils import generation_utils
        temp = temperature if temperature is not None else self.exp_config.temperature
        model = self.model_name

        if "gpt" in model or "o1" in model or "o3" in model or "o4" in model:
            # OpenAI gpt-4o supports max 16384 completion tokens
            capped_tokens = min(max_output_tokens, 16384)
            config = {
                "system_prompt": self.system_prompt,
                "temperature": temp,
                "candidate_num": candidate_count,
                "max_completion_tokens": capped_tokens,
            }
            return await generation_utils.call_openai_with_retry_async(
                model_name=model, contents=contents, config=config,
                max_attempts=max_attempts, retry_delay=retry_delay,
            )
        elif "claude" in model:
            config = {
                "system_prompt": self.system_prompt,
                "temperature": temp,
                "candidate_num": candidate_count,
                "max_output_tokens": max_output_tokens,
            }
            return await generation_utils.call_claude_with_retry_async(
                model_name=model, contents=contents, config=config,
                max_attempts=max_attempts, retry_delay=retry_delay,
            )
        else:
            # Default: Gemini
            from google.genai import types
            return await generation_utils.call_gemini_with_retry_async(
                model_name=model, contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=temp,
                    candidate_count=candidate_count,
                    max_output_tokens=max_output_tokens,
                ),
                max_attempts=max_attempts, retry_delay=retry_delay,
            )

    @abstractmethod
    async def process(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Process the input data and return the result.
        
        Args:
            data: Input data dictionary
            **kwargs: Additional subclass-specific parameters
        
        Returns:
            Processed data dictionary
        """

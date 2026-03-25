# What
- I want to add alibaba cloud provider:
  - use the same openai api
  - based url: https://coding-intl.dashscope.aliyuncs.com/v1
  - models: glm-5, kimi-k2.5, qwen3.5-plus, minimax
- I want to add separate configuration for embedding model.
  - use the same openai api
  - based url: https://dashscope-intl.aliyuncs.com/compatible-mode/v1

# How
- Check frontend source code to understand what need to be done
- Check backend python source code (folder src) to understand what need to be done
- Add Alibaba cloud provider to frontend
- Add custom embedding configuration to frontend
- 
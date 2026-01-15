---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

## 🎓 Education (教育背景)

*   **National University of Singapore (NUS)**
    *   Master of Science in Energy Systems
    *   2023 - 2024
    *   *Focus: Renewable Energy, Energy Systems*

*   **Shanghai Jiao Tong University (SJTU)**
    *   Bachelor of Engineering in Biomedical Engineering
    *   2018 - 2022
    *   *Note: Transferred to **Smart Energy Innovation Institute** in 2022 for senior training (Focus: New Energy + AI)*

## 💼 Work Experience (工作经历)

*   **Machine Learning Engineer** | **GCL Group (协鑫集团)**
    *   2025 - Present
    *   **Responsibilities**:
        *   **Energy Optimization**: Designed and implemented optimization scheduling strategies for Virtual Power Plants (VPP) and source-grid-load-storage systems.
        *   **Time Series Prediction**: Developed high-precision models for power load forecasting and renewable energy (PV/Wind) generation prediction.
        *   **AI Applications**: Led the development of "ChatData" (LLM-based data analysis platform) and smart meeting assistants.

*   **Algorithm Engineer Intern** | **Trina Solar International Research Center (Singapore)**
    *   2024 - 2025
    *   **Responsibilities**:
        *   **Insight & Analysis**: Conducted industry trend analysis and defined model development directions based on customer requirements.
        *   **Data Engineering**: Managed data collection (PV, wind, load, price) for the Australian market; deployed cloud servers for data transmission; built cross-platform (Win/Linux) data pipelines.
        *   **Optimization**: Evaluated performance of various solvers (Cplex, Gurobi, SCIP, GLPK) using Python/Julia.
        *   **Modeling**: Developed optimization models using **Pyomo** to provide decision support for energy storage system scheduling.

## 🔬 Research Experience (科研经历)

*   **Research Assistant** | **SJTU Smart Energy Innovation Institute (Liu Zuming Group)**
    *   2021 - 2024
    *   **Focus**: Photovoltaic power time series prediction using deep learning and spatiotemporal analysis.
    *   **Achievements**: Published research in *Energy and AI* and multiple international conferences.

## 🛠️ Skills (技能专长)

*   **Programming & Tools**: Python, PyTorch, TensorFlow, SQL, Git.
*   **Core Competencies**: Machine Learning, Deep Learning, Time Series Forecasting, Mathematical Optimization, Large Language Models (LLM), Energy System Modeling.

## 💡 Patents & Softwares (专利与软著)

*   **一种基于时间维度的电力价格预测方法、装置、设备及存储介质** (CN121120113A)
*   **一种光伏发电功率预测方法及系统** (CN120069194A)
*   **融合时空关系的太阳能光伏发电功率预测方法** (CN118569423A)
*   **超参数自优化及结构自调整的超短期光伏输出预测方法** (CN117454934A)
*   *And several software copyrights (持有若干软件著作权).*

## 📝 Publications (发表论文)

<ul>{% for post in site.publications reversed %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>

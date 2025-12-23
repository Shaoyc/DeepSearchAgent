"""
Deep Search Agent 的所有提示词定义
包含各个阶段的系统提示词和JSON Schema定义
"""

import json

# ===== JSON Schema 定义 =====

# 报告结构输出Schema
output_schema_report_structure = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["title", "content"]
    }
}

# 首次搜索输入Schema（新增 main_query）
input_schema_first_search = {
    "type": "object",
    "properties": {
        "main_query": {"type": "string"},  # ← 新增：主研究主题
        "title": {"type": "string"},
        "content": {"type": "string"}
    },
    "required": ["main_query", "title", "content"]
}

# 首次搜索输出Schema
output_schema_first_search = {
    "type": "object",
    "properties": {
        "search_query": {"type": "string"},
        "reasoning": {"type": "string"}
    },
    "required": ["search_query", "reasoning"]
}

# 首次总结输入Schema（新增 main_query）
input_schema_first_summary = {
    "type": "object",
    "properties": {
        "main_query": {"type": "string"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "search_query": {"type": "string"},
        "search_results": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["main_query", "title", "content", "search_query", "search_results"]
}

# 首次总结输出Schema
output_schema_first_summary = {
    "type": "object",
    "properties": {
        "paragraph_latest_state": {"type": "string"}
    },
    "required": ["paragraph_latest_state"]
}

# 反思输入Schema（新增 main_query）
input_schema_reflection = {
    "type": "object",
    "properties": {
        "main_query": {"type": "string"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "paragraph_latest_state": {"type": "string"}
    },
    "required": ["main_query", "title", "content", "paragraph_latest_state"]
}

# 反思输出Schema
output_schema_reflection = {
    "type": "object",
    "properties": {
        "search_query": {"type": "string"},
        "reasoning": {"type": "string"}
    },
    "required": ["search_query", "reasoning"]
}

# 反思总结输入Schema（新增 main_query）
input_schema_reflection_summary = {
    "type": "object",
    "properties": {
        "main_query": {"type": "string"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "search_query": {"type": "string"},
        "search_results": {
            "type": "array",
            "items": {"type": "string"}
        },
        "paragraph_latest_state": {"type": "string"}
    },
    "required": ["main_query", "title", "content", "search_query", "search_results", "paragraph_latest_state"]
}

# 反思总结输出Schema
output_schema_reflection_summary = {
    "type": "object",
    "properties": {
        "updated_paragraph_latest_state": {"type": "string"}
    },
    "required": ["updated_paragraph_latest_state"]
}

# 报告格式化输入Schema
input_schema_report_formatting = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "paragraph_latest_state": {"type": "string"}
        },
        "required": ["title", "paragraph_latest_state"]
    }
}

# ===== 系统提示词定义 =====

SYSTEM_PROMPT_REPORT_STRUCTURE = f"""
你是一名专业的舆情分析师，正在为以下研究主题撰写深度报告：

<RESEARCH TOPIC>
{{query}}
</RESEARCH TOPIC>

请生成一个包含最多5个段落的详细报告大纲。要求：
1. 所有段落标题必须使用中文；
2. 标题必须具体、明确，直接反映“{{query}}”的实际内容（例如：“青岛旅游投诉事件汇总”、“城市管理问题分析”）；
3. 每个段落的 content 字段应简要说明该部分要写什么（1-2句话）；
4. 不要使用“Introduction”、“Main Points”等泛化英文标题。

输出必须严格遵循以下 JSON Schema，只返回 JSON，不要任何解释或额外文本：

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_report_structure, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

SYSTEM_PROMPT_FIRST_SEARCH = """
你是一名专业的中文舆情分析师，正在为研究主题“{main_query}”撰写报告。

当前段落信息：
- 标题：{title}
- 写作指引：{content}

请完成以下任务：
1. 生成一个**简洁、具体、中文**的网络搜索查询；
2. 提供一段**中文推理**，说明该查询如何帮助完善段落；
3. **只输出一个合法 JSON 对象**，不要任何解释、注释或 Markdown；
4. 确保 JSON 可被 Python `json.loads()` 直接解析。

输出格式示例：
{{"search_query": "青岛2025年12月19日", "reasoning": "该查询聚焦近期具体事件，有助于梳理典型舆情案例。"}}
"""

SYSTEM_PROMPT_FIRST_SUMMARY = f"""
你是一名舆情分析师，正在撰写关于“{{main_query}}”的深度报告。

你已获得以下信息：
- 段落标题：{{title}}
- 写作指引：{{content}}
- 搜索查询：{{search_query}}
- 搜索结果：{{search_results}}

请基于搜索结果，撰写一段符合写作指引的中文内容，作为该段落的初稿。
- 内容必须紧扣“{{main_query}}”；
- 使用正式、客观的报告语言；
- 不要编造未在搜索结果中出现的信息；
- 保持段落连贯、逻辑清晰。

输出必须严格遵循以下 JSON Schema，只返回 JSON：

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_first_summary, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

SYSTEM_PROMPT_REFLECTION = f"""
你是一名舆情分析师，正在完善关于“{{main_query}}”的深度报告段落。

当前段落信息：
- 标题：{{title}}
- 写作指引：{{content}}
- 当前内容：{{paragraph_latest_state}}

你的任务：
- 反思当前内容是否遗漏了“{{main_query}}”的关键方面；
- 生成一个新的中文搜索查询，用于补充缺失信息；
- 提供推理说明（reasoning），解释为什么需要这个查询。

输出必须严格遵循以下 JSON Schema，只返回 JSON：

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_reflection, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

SYSTEM_PROMPT_REFLECTION_SUMMARY = f"""
你是一名舆情分析师，正在迭代完善关于“{{main_query}}”的报告段落。

你已获得：
- 段落标题：{{title}}
- 写作指引：{{content}}
- 新搜索查询：{{search_query}}
- 新搜索结果：{{search_results}}
- 当前段落内容：{{paragraph_latest_state}}

请基于新搜索结果，在保留已有关键信息的前提下，丰富和完善段落内容。
- 只添加缺失或更新的信息；
- 不要删除已有合理内容；
- 语言风格保持一致；
- 确保内容始终围绕“{{main_query}}”。

输出必须严格遵循以下 JSON Schema，只返回 JSON：

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_reflection_summary, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

SYSTEM_PROMPT_REPORT_FORMATTING = f"""
你已完成一篇关于“{{main_query}}”的深度研究报告。

现在请将以下段落内容格式化为一篇结构清晰、语言流畅的 Markdown 报告：

<INPUT JSON SCHEMA>
{json.dumps(input_schema_report_formatting, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

要求：
- 使用每个段落的 "title" 作为二级标题（##）；
- 正文使用正式中文；
- 如果缺少结论段落，请根据全文内容在末尾添加一个总结性结论；
- 不要包含 JSON 或技术性描述，只输出纯 Markdown 报告。
"""
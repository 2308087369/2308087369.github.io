#!/usr/bin/env python3
"""Generate a clean 2-page Chinese resume PDF for Bo Chen."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------- fonts ----------
FONT_REG = "MSYH"
FONT_BOLD = "MSYH-Bold"
FONT_LIGHT = "MSYH-Light"

pdfmetrics.registerFont(TTFont(FONT_REG, r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont(FONT_LIGHT, r"C:\Windows\Fonts\msyhl.ttc", subfontIndex=0))
pdfmetrics.registerFontFamily(
    "MSYH", normal=FONT_REG, bold=FONT_BOLD, italic=FONT_REG, boldItalic=FONT_BOLD
)

# ---------- palette ----------
NAVY = colors.HexColor("#1a365d")
ACCENT = colors.HexColor("#2b6cb0")
TEXT = colors.HexColor("#1a202c")
MUTED = colors.HexColor("#4a5568")
LINE = colors.HexColor("#cbd5e0")
SOFT = colors.HexColor("#edf2f7")

PAGE_W, PAGE_H = A4
LEFT = 16 * mm
RIGHT = 16 * mm
TOP = 12 * mm
BOTTOM = 12 * mm

# ---------- styles ----------
def S(name, **kw):
    base = dict(
        fontName=FONT_REG, fontSize=9, leading=13.5, textColor=TEXT,
        spaceBefore=0, spaceAfter=0, alignment=TA_LEFT,
    )
    base.update(kw)
    return ParagraphStyle(name, **base)

st_name = S("name", fontName=FONT_BOLD, fontSize=22, leading=28, textColor=NAVY)
st_name_en = S("name_en", fontName=FONT_LIGHT, fontSize=13, leading=18, textColor=MUTED)
st_title = S("title", fontName=FONT_BOLD, fontSize=10.5, leading=15, textColor=ACCENT)
st_contact = S("contact", fontName=FONT_REG, fontSize=8.5, leading=13, textColor=MUTED)
st_section = S("section", fontName=FONT_BOLD, fontSize=11.5, leading=16, textColor=NAVY, spaceBefore=7, spaceAfter=3)
st_job_head = S("job_head", fontName=FONT_BOLD, fontSize=10, leading=14, textColor=TEXT)
st_job_meta = S("job_meta", fontName=FONT_REG, fontSize=8.5, leading=12, textColor=MUTED)
st_body = S("body", fontSize=9, leading=13.2, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
st_bullet = S("bullet", fontSize=9, leading=13.0, textColor=TEXT, leftIndent=10, firstLineIndent=-8, spaceAfter=1.5, wordWrap="CJK", splitLongWords=0)
st_pub = S("pub", fontSize=8.2, leading=11.5, textColor=TEXT, leftIndent=10, firstLineIndent=-10, spaceAfter=2, wordWrap="CJK", splitLongWords=0)
st_small = S("small", fontSize=8, leading=11.5, textColor=MUTED, wordWrap="CJK")
st_sub = S("sub", fontName=FONT_BOLD, fontSize=9, leading=12.5, textColor=ACCENT, spaceBefore=2, spaceAfter=1, wordWrap="CJK")
st_skill = S("skill", fontSize=8.8, leading=12.5, textColor=TEXT, wordWrap="CJK")


def section(title, *follow):
    """Section header kept with the following block so it never orphans on a page."""
    block = [
        Spacer(1, 2 * mm),
        Paragraph(title, st_section),
        HRFlowable(width="100%", thickness=1.1, color=ACCENT, spaceBefore=1, spaceAfter=3.5),
    ]
    block.extend(follow)
    return [KeepTogether(block)]


def job_header(role, org, date, location=""):
    left = Paragraph(f"{role}<font color='#4a5568'>　|　</font>{org}", st_job_head)
    right = Paragraph(date if not location else f"{date}<br/>{location}", st_job_meta)
    right.alignment = TA_RIGHT
    t = Table([[left, right]], colWidths=[115 * mm, 55 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t


def bullets(items, style=None):
    style = style or st_bullet
    return [Paragraph(f"•　{item}", style) for item in items]


def header_footer(canvas, doc):
    canvas.saveState()
    # thin top accent bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 3.2 * mm, PAGE_W, 3.2 * mm, fill=1, stroke=0)
    # footer
    canvas.setFont(FONT_LIGHT, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(LEFT, 8 * mm, "陈波 · 机器学习工程师 · AI + 能源")
    canvas.drawRightString(PAGE_W - RIGHT, 8 * mm, f"第 {doc.page} 页 / 共 2 页")
    canvas.restoreState()


def build(path):
    doc = BaseDocTemplate(
        path, pagesize=A4,
        leftMargin=LEFT, rightMargin=RIGHT,
        topMargin=TOP + 2 * mm, bottomMargin=BOTTOM + 2 * mm,
        title="陈波 Bo Chen — 机器学习工程师简历",
        author="Bo Chen",
        subject="机器学习工程师 / AI + 能源 / 虚拟电厂",
    )
    frame = Frame(
        LEFT, BOTTOM + 4 * mm,
        PAGE_W - LEFT - RIGHT, PAGE_H - TOP - BOTTOM - 8 * mm,
        id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=header_footer)])

    story = []
    content_w = PAGE_W - LEFT - RIGHT

    # ===== header =====
    name_row = Table(
        [[
            Paragraph("陈波　Bo Chen", st_name),
            Paragraph("成都 · 四川", st_contact),
        ]],
        colWidths=[content_w * 0.7, content_w * 0.3],
    )
    name_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(name_row)
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("机器学习工程师　·　AI + 能源　·　虚拟电厂 / 电力市场 / 时序预测", st_title))
    story.append(Spacer(1, 1.2 * mm))
    contact_row = Table(
        [[
            Paragraph("Email: <link href='mailto:bo_chen@u.nus.edu' color='#4a5568'>bo_chen@u.nus.edu</link>", st_contact),
            Paragraph("GitHub: <link href='https://github.com/2308087369' color='#4a5568'>2308087369</link>", st_contact),
            Paragraph("CSDN: <link href='https://blog.csdn.net/qq_43743777' color='#4a5568'>qq_43743777</link>", st_contact),
            Paragraph("Scholar: <link href='https://scholar.google.com/citations?user=j8RCF8sAAAAJ' color='#4a5568'>j8RCF8sAAAAJ</link>", st_contact),
        ]],
        colWidths=[content_w * 0.32, content_w * 0.22, content_w * 0.22, content_w * 0.24],
    )
    contact_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(contact_row)
    story.append(Spacer(1, 1.5 * mm))
    story.append(HRFlowable(width="100%", thickness=1.8, color=NAVY, spaceBefore=0, spaceAfter=2))

    # ===== summary =====
    story += section("个人概要")
    story.append(Paragraph(
        "专注 <b>AI + 能源</b> 方向，具备能源系统建模、时间序列预测、数学优化与大模型应用的完整工程经验。"
        "能独立覆盖从需求分析、算法研发、模型封装到生产部署的全链路，推动虚拟电厂、电力市场与源网荷储能力真实可用、可运营。"
        "曾作为产品经理与算法负责人从零到一交付省级虚拟电厂平台，在新加坡天合光能完成海外能源数据与储能调度优化工作，"
        "并在上海交通大学从事光伏功率预测研究，成果发表于 <i>Energy and AI</i> 等期刊与国际会议。",
        st_body,
    ))

    # ===== work =====
    story += section("工作经历")

    story.append(job_header("机器学习工程师", "协鑫集团子公司", "2025 – 至今", "成都"))
    story.append(Spacer(1, 0.8 * mm))
    story += bullets([
        "<b>能源优化调度</b>：设计并落地源网荷储协同优化调度策略，开发虚拟电厂聚合调度算法，提升系统经济性与响应能力。",
        "<b>时间序列预测</b>：研发电力负荷、风电/光伏出力的短临与超短期预测模型，支撑日前/实时调度与新能源消纳。",
        "<b>AI 应用落地</b>：主导 ChatData 大模型数据交互平台、智能会议助手与自动化分析流水线，推动 AI 能力服务业务决策。",
    ])
    story.append(Spacer(1, 1.2 * mm))
    story.append(Paragraph("代表项目：福建省某虚拟电厂平台　|　产品经理 & 算法负责人", st_sub))
    story += bullets([
        "<b>从零到一交付</b>：负责产品规划、需求拆解、架构设计、开发协同、测试验收与生产部署，推动平台从概念走向真实业务运行。",
        "<b>平台对接与数据闭环</b>：完成交易中心开放平台、负管中心物联管理平台对接，打通资源接入、数据处理、状态监测与可视化链路。",
        "<b>业务场景落地</b>：实现虚拟电厂需求响应与现货交易能力，支撑聚合资源参与电力市场业务。",
        "<b>时序预测体系</b>：负责日前/实时双市场价格、风电光伏、代理用户负荷预测的算法选型、特征与模型优化、接口封装及工程化部署。",
        "<b>国产化部署</b>：完成算法服务在信创服务器上的适配、封装与部署，保障模型在生产环境稳定运行。",
    ])

    story.append(Spacer(1, 2.5 * mm))
    story.append(job_header("算法工程师", "天合光能国际研究中心（新加坡）", "2024 – 2025", "Singapore"))
    story.append(Spacer(1, 0.8 * mm))
    story += bullets([
        "<b>需求洞察</b>：开展行业技术趋势分析，结合客户业务需求确定模型开发方向。",
        "<b>数据工程</b>：负责澳洲区域光伏、风电、负荷与电价数据采集处理；搭建云服务器完成数据传输；构建 Windows\u00a0/\u00a0Linux 跨平台数据流水线。",
        "<b>优化建模</b>：评估 Cplex / Gurobi / SCIP / GLPK 等求解器在 Python / Julia 环境下的性能；基于 <b>Pyomo</b> 搭建储能调度优化模型，提供科学决策支持。",
    ])

    # ===== education =====
    story += section("教育背景")
    edu_data = [
        [
            Paragraph("<b>新加坡国立大学（NUS）</b>", st_job_head),
            Paragraph("2023 – 2024", st_job_meta),
        ],
        [
            Paragraph("理学硕士 · 能源系统（M.S. Energy Systems）　|　方向：可再生能源、能源系统", st_body),
            Paragraph("", st_job_meta),
        ],
        [
            Paragraph("<b>上海交通大学（SJTU）</b>", st_job_head),
            Paragraph("2018 – 2022", st_job_meta),
        ],
        [
            Paragraph("工学学士 · 生物医学工程（B.Eng.）　|　2021 年转入智慧能源创新学院（新能源 + AI）", st_body),
            Paragraph("", st_job_meta),
        ],
    ]
    edu_t = Table(edu_data, colWidths=[content_w * 0.78, content_w * 0.22])
    edu_t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(edu_t)

    # ===== research =====
    story += section("科研经历")
    story.append(job_header("研究助理", "上海交通大学智慧能源创新学院（刘祖明课题组）", "2021 – 2024"))
    story.append(Spacer(1, 0.8 * mm))
    story += bullets([
        "聚焦光伏发电功率时间序列预测，提出时空关系融合网络（Spatiotemporal Relation Fused Network），显著提升预测精度。",
        "学位论文：<i>A novel spatiotemporal relation fused network for solar photovoltaic power forecasting</i>。",
        "成果发表于 <i>Energy and AI</i>，并在 EPEE、IET 等国际会议作口头报告 / 发表会议论文。",
    ])

    # ===== publications =====
    pubs = [
        "<b>[Energy and AI, 2026]</b>　A novel spatiotemporal relation fused network for solar photovoltaic power forecasting.　<i>Z Liu, S Li, J Ding, Y Zheng, <b>B Chen</b> (通讯), Y He</i>",
        "<b>[IET CP934, 2025]</b>　A novel spatiotemporal relation fused network for solar photovoltaic power prediction.　<i>L Tang, <b>B Chen</b>, Z Liu</i>",
        "<b>[EPEE 2024]</b>　High-resolution Photovoltaic Power Prediction based on Dynamic Time Constants Residual Recurrent Neural Network.　<i><b>B Chen</b>, H Jiang, Y Sheng</i>",
        "<b>[Energy, 2024]</b>　Optimal Transition Pathway of Power Systems for Guangdong-Hongkong-Macau Region in China.　<i>Y Zhao, L Tang, <b>B Chen</b>, Z Liu</i>",
    ]
    pub_flowables = [Paragraph(p, st_pub) for p in pubs]
    story += section("代表性论文", *pub_flowables)

    # ===== patents =====
    story += section("发明专利与软著")
    story.append(Paragraph("<b>已授权 / 公开发明专利</b>", st_sub))
    story.append(Paragraph(
        "1. 一种基于时间维度的电力价格预测方法、装置、设备及存储介质（CN121120113A）<br/>"
        "2. 一种光伏发电功率预测方法及系统（CN120069194A）<br/>"
        "3. 融合时空关系的太阳能光伏发电功率预测方法（CN118569423A）<br/>"
        "4. 超参数自优化及结构自调整的超短期光伏输出预测方法（CN117454934A）",
        st_body,
    ))
    story.append(Paragraph("<b>2026 年在审发明专利（第一发明人）</b>", st_sub))
    story.append(Paragraph(
        "1. 一种电力负荷预测方法、装置、设备及介质（申请号 202610298514.2，实质审查）<br/>"
        "2. 一种虚拟电厂资源调度方法、装置、设备及存储介质（申请号 202610858814.1，实质审查）<br/>"
        "3. 一种充电站柔性负荷调度方法、装置、设备及介质（申请号 202610864467.3，实质审查）",
        st_body,
    ))
    story.append(Paragraph("另持有若干项软件著作权。", st_body))

    # ===== skills =====
    story += section("核心技能")
    skill_rows = [
        ["能源 AI", "虚拟电厂聚合调度、需求响应、现货交易、源网荷储协同优化、电力市场建模与业务落地"],
        ["预测算法", "电价 / 负荷 / 风电 / 光伏功率预测；日前—实时—超短期多尺度时序建模与特征工程"],
        ["优化求解", "数学规划与混合整数优化；Pyomo 建模；Cplex / Gurobi / SCIP / GLPK（Python / Julia）"],
        ["机器学习", "PyTorch、TensorFlow、深度学习、时序模型、模型调参、评估与工程化封装"],
        ["大模型应用", "LLM 数据分析平台（ChatData）、智能会议助手、Prompt 工程、RAG / Agent 落地实践"],
        ["工程与部署", "Python、SQL、Git、Linux、云服务器、跨平台数据流水线、API 封装、信创环境部署"],
    ]
    skill_data = [[Paragraph(f"<b>{k}</b>", st_skill), Paragraph(v, st_skill)] for k, v in skill_rows]
    skill_t = Table(skill_data, colWidths=[28 * mm, content_w - 28 * mm])
    skill_t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4),
        ("BACKGROUND", (0, 0), (0, -1), SOFT),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [colors.white, colors.HexColor("#f7fafc")]),
    ]))
    story.append(skill_t)

    # ===== highlights =====
    story += section("职业亮点")
    story += bullets([
        "<b>产研一体</b>：既有省级虚拟电厂从零到一的产品与算法负责经验，也有海外研究中心的能源优化建模经历，能同时对齐业务目标与技术方案。",
        "<b>全链路交付</b>：覆盖数据接入、算法研发、接口封装、信创部署与生产运维，具备把模型真正做成线上服务的工程能力。",
        "<b>成果沉淀</b>：公开发明专利 4 项、在审发明专利 3 项（第一发明人），发表 SCI / 国际会议论文多篇，形成“预测—优化—调度”技术闭环。",
    ])

    # ===== extras =====
    story += section("开源项目与技术分享")
    story += bullets([
        "<b>Virtual Power Plants</b>（github.com/2308087369/Virtual-power-plants）：面向虚拟电厂优化调度的开源项目，提供负荷、光伏、风电数据生成模块与优化调度求解器。",
        "<b>CSDN 技术博客</b>（blog.csdn.net/qq_43743777）：持续输出优化转强化学习（OPT-to-RL）、虚拟电厂调度优化系统、Prompt 工程架构等技术文章。",
        "<b>个人主页</b>（2308087369.github.io）：汇总研究论文、专利成果、开源项目与研究方向，便于了解完整技术背景。",
    ])

    story.append(Spacer(1, 2.5 * mm))
    story.append(Paragraph(
        "语言能力：中文（母语）　·　英语（流利；新加坡国立大学硕士 / 新加坡全职工作经历）　　"
        "求职方向：机器学习 / 能源 AI / 虚拟电厂算法相关岗位",
        st_small,
    ))

    doc.build(story)
    print(f"wrote {path}")


if __name__ == "__main__":
    build(r"D:\py_work\bochen1024.github.io\files\简历-陈波-2026.pdf")

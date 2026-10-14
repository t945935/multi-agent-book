// 出版級書籍封面 Typst 模板 (Book Cover Template)

#set page(
  paper: "iso-b5",
  margin: (x: 2.5cm, y: 3cm),
  fill: rgb("#0f172a") // 深邃科技黑藍底色
)

#set text(
  font: ("Noto Sans CJK TC", "Noto Sans TC", "DejaVu Sans"),
  fill: white,
  lang: "zh"
)

#align(center + top)[
  #v(2cm)
  #text(size: 11pt, tracking: 4pt, fill: rgb("#38bdf8"), weight: "bold")[MULTI-AGENT ARCHITECTURE & PRACTICE]
  #v(1.2cm)
  
  #text(size: 26pt, weight: "bold", fill: white)[多 Agent 系統架構與實戰]
  #v(0.8cm)
  
  #text(size: 14pt, fill: rgb("#94a3b8"))[用 AI Agent 團隊完成寫作、測試、排版與發布]
  #v(2cm)
  
  // 科技幾何裝飾框
  #rect(
    width: 6cm,
    height: 1pt,
    fill: gradient.linear(rgb("#38bdf8"), rgb("#818cf8"))
  )
  
  #v(3cm)
  #text(size: 11pt, fill: rgb("#cbd5e1"))[
    *作者*：Happy eBook Authors  
    #v(0.3cm)
    *技術審查*：Hermes · Codex · OpenCode · Pi
  ]
]

#align(center + bottom)[
  #text(size: 9pt, fill: rgb("#64748b"))[
    2026 EDITION · FULLY AUTOMATED CI/CD RELEASE
  ]
  #v(1cm)
]

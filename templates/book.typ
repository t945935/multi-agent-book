// 現代科技書 Typst 排版樣式模板 (Typst Tech Book Template)

#let project(
  title: "書籍標題",
  subtitle: "書籍副標題",
  author: "作者團隊",
  version: "1.0.0",
  body
) = {
  // 設定頁面尺寸與邊界 (採用 ISO-B5 科技書標準版面)
  set page(
    paper: "iso-b5",
    margin: (inside: 2.2cm, outside: 1.8cm, top: 2.2cm, bottom: 2.2cm),
    header: context {
      let page_number = counter(page).get().first()
      if page_number > 2 {
        align(center)[
          #text(size: 8.5pt, fill: luma(120))[#title · #subtitle]
          #v(-4pt)
          #line(length: 100%, stroke: 0.5pt + luma(200))
        ]
      }
    },
    footer: context {
      let page_number = counter(page).get().first()
      if page_number > 2 {
        align(center)[#text(size: 9pt, fill: luma(100))[#page_number]]
      }
    }
  )

  // 設定正文字型與字級
  set text(
    font: ("Noto Sans CJK TC", "Noto Sans TC", "DejaVu Sans"),
    size: 10pt,
    lang: "zh"
  )

  // 設定段落縮排與行距
  set par(
    justify: true,
    leading: 0.75em,
    first-line-indent: 0em
  )

  // 設定標題樣式
  show heading.where(level: 1): it => block(width: 100%, breakable: false)[
    #v(1.5em)
    #text(size: 18pt, weight: "bold", fill: rgb("#1a365d"))[#it.body]
    #v(0.6em)
    #line(length: 100%, stroke: 1.5pt + rgb("#3182ce"))
    #v(1em)
  ]

  show heading.where(level: 2): it => block(breakable: false)[
    #v(1.2em)
    #text(size: 13pt, weight: "bold", fill: rgb("#2b6cb0"))[#it.body]
    #v(0.5em)
  ]

  show heading.where(level: 3): it => block(breakable: false)[
    #v(1em)
    #text(size: 11pt, weight: "bold", fill: rgb("#2d3748"))[#it.body]
    #v(0.3em)
  ]

  // 設定代碼區塊樣式
  show raw.where(block: true): it => block(
    width: 100%,
    fill: rgb("#f7fafc"),
    stroke: 0.5pt + rgb("#e2e8f0"),
    inset: 10pt,
    radius: 4pt,
    breakable: true
  )[
    #set text(font: "DejaVu Sans Mono", size: 8.5pt)
    #it
  ]

  // 引用塊樣式 (Callout / Blockquote)
  show quote: it => rect(
    width: 100%,
    fill: rgb("#ebf8ff"),
    stroke: (left: 3pt + rgb("#3182ce")),
    inset: (x: 10pt, y: 8pt),
    radius: (right: 4pt)
  )[
    #text(style: "italic", fill: rgb("#2b6cb0"))[#it.body]
  ]

  // 輸出正文
  body
}

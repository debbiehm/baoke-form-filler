# 保客填表 · Nomination Form Filler

A single-page web app that fills Great Eastern's **Appointment / Change of Nominee(s) / Trustee(s)** form
(NBZ-FNOMI-V07-082025) and checks it against the form's own notes before you print.

**Open it:** https://&lt;your-github-username&gt;.github.io/&lt;repo&gt;/ on a phone or computer, or download `index.html` and open it in Chrome / Edge.

## What it does

- **Read a policy:** upload a GE e-policy PDF (password supported), a scan or a photo. It captures the Policy No, the policyowner's name, NRIC and address, and you confirm before anything is filled in.
- **Bulk upload:** Excel / CSV with one client per row (press 下载批量模板 for the template).
- **Checks:** shares add up to 100%, Muslim / non-Muslim trust rules (notes 1–4), NRIC vs date of birth and gender, trustee and witness age, passport expiry, and box lengths.
- **Output:** preview, print, or export PDF (one client, or all as a ZIP).
- Signatures, signature dates and Part 3 are left for handwriting on purpose.

## Privacy

Everything runs in your browser. Client details are saved only in that browser (localStorage) and are never uploaded.
Photos and scans need internet once to download the text-recognition engine (tesseract.js); the document itself stays on the device.
Use **导出资料 Excel** to back up, and **⚙ 设定 → 清除全部保客资料** on shared devices.

Set your own agent name and IAC No in **⚙ 设定** on each device (used when you are the witness).

## Rebuilding

`index.html` is generated. After editing `web/template.html` or `layout.py`:

```bash
pip install pymupdf
python web/build_html.py
```

The build measures the form's boxes (`boxes.py`), embeds the blank form, the box positions and the libraries
(pdf-lib, pdf.js, SheetJS, JSZip in `web/vendor/`), so the page works offline.

If Great Eastern releases a new form version, the box positions in `layout.py` must be re-checked.

## Notice

Not affiliated with or endorsed by Great Eastern Life Assurance (Malaysia) Berhad. The blank form is
Great Eastern's document, included only so the filled copy matches the official layout. Always check the
filled form against the client's NRIC before submission.

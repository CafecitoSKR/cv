import html
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Falta PyYAML. Instálalo con:  pip install pyyaml")

BASE = Path(__file__).resolve().parent
DATA = BASE / "cv-data.yaml"
OUT = BASE / "index.html"


def e(text):
    return html.escape(str(text)) if text is not None else ""


def build(d):
    c = d.get("contacto", {})

    partes = []
    if d.get("ubicacion"):
        partes.append(e(d["ubicacion"]))
    if c.get("telefono"):
        partes.append(e(c["telefono"]))
    if c.get("email"):
        partes.append(f'<a href="mailto:{e(c["email"])}">{e(c["email"])}</a>')
    if c.get("linkedin"):
        partes.append(f'<a href="https://{e(c["linkedin"])}">{e(c["linkedin"])}</a>')
    if c.get("github"):
        partes.append(f'<a href="https://{e(c["github"])}">{e(c["github"])}</a>')
    contacto_html = ' &nbsp;|&nbsp; '.join(partes)

    exp_items = []
    for x in d.get("experiencia", []):
        logros = "".join(f"<li>{e(l)}</li>" for l in x.get("logros", []))
        sub = " — ".join(filter(None, [e(x.get("cargo")), e(x.get("ubicacion"))]))
        exp_items.append(f"""
        <div class="entry">
          <div class="entry-head">
            <span class="org">{e(x.get('empresa'))}</span>
            <span class="dates">{e(x.get('periodo'))}</span>
          </div>
          <div class="sub">{sub}</div>
          <ul>{logros}</ul>
        </div>""")
    exp_html = "".join(exp_items)

    edu_items = []
    for x in d.get("educacion", []):
        edu_items.append(f"""
        <div class="entry">
          <div class="entry-head">
            <span class="org">{e(x.get('institucion'))}</span>
            <span class="dates">{e(x.get('periodo'))}</span>
          </div>
          <div class="sub">{e(x.get('titulo'))}</div>
        </div>""")
    edu_html = "".join(edu_items)

    skill_rows = []
    for cat, items in d.get("habilidades", {}).items():
        skill_rows.append(f'<div class="skill-line"><b>{e(cat)}:</b> {e(", ".join(items))}</div>')
    skills_html = "".join(skill_rows)

    idiomas_html = e(" · ".join(d.get("idiomas", [])))
    certs_html = "".join(f"<li>{e(i)}</li>" for i in d.get("certificaciones", []))

    return TEMPLATE.format(
        nombre=e((d.get("nombre") or "").upper()),
        titular=e(d.get("titular")),
        contacto=contacto_html,
        resumen=e((d.get("resumen") or "").strip()),
        experiencia=exp_html,
        educacion=edu_html,
        habilidades=skills_html,
        idiomas=idiomas_html,
        certificaciones=certs_html,
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>CV — {nombre}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Georgia", "Times New Roman", serif;
    color: #000;
    line-height: 1.38;
    font-size: 11pt;
    background: #e9e9e9;
  }}
  .page {{
    width: 8.5in;
    min-height: 11in;
    margin: 24px auto;
    background: #fff;
    padding: 0.7in 0.8in;
    box-shadow: 0 2px 14px rgba(0,0,0,.18);
  }}
  header {{ text-align: center; margin-bottom: 16px; }}
  h1 {{ font-size: 20pt; letter-spacing: 2px; font-weight: bold; }}
  .titular {{ font-size: 10.5pt; font-style: italic; margin-top: 3px; }}
  .contacto {{ font-size: 9.5pt; margin-top: 6px; }}
  .contacto a {{ color: #000; text-decoration: none; }}
  section {{ margin-top: 14px; }}
  h2 {{
    font-size: 11pt; text-transform: uppercase; letter-spacing: 1px;
    font-weight: bold; border-bottom: 1.2px solid #000;
    padding-bottom: 2px; margin-bottom: 8px;
  }}
  .resumen {{ text-align: justify; }}
  .entry {{ margin-bottom: 11px; }}
  .entry:last-child {{ margin-bottom: 0; }}
  .entry-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
  .org {{ font-weight: bold; }}
  .dates {{ font-style: italic; font-size: 10pt; white-space: nowrap; }}
  .sub {{ font-style: italic; margin: 1px 0 4px; }}
  ul {{ padding-left: 18px; margin-top: 2px; }}
  li {{ margin-bottom: 2px; text-align: justify; }}
  .skill-line {{ margin-bottom: 3px; }}
  .dl-btn {{
    position: fixed; top: 20px; right: 20px;
    background: #16526e; color: #fff; text-decoration: none;
    font-family: -apple-system, "Segoe UI", sans-serif; font-size: 10pt;
    padding: 10px 16px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,.25);
    z-index: 100;
  }}
  .dl-btn:hover {{ background: #1d6a8f; }}
  @media print {{
    body {{ background: #fff; }}
    .page {{ box-shadow: none; margin: 0; width: auto; min-height: auto; padding: 0; }}
    section, .entry {{ page-break-inside: avoid; }}
    .dl-btn {{ display: none; }}
  }}
  @page {{ size: letter; margin: 0.7in 0.8in; }}
</style>
</head>
<body>
  <a class="dl-btn" href="cv.pdf" download>⬇ Descargar PDF</a>
  <div class="page">
    <header>
      <h1>{nombre}</h1>
      <div class="titular">{titular}</div>
      <div class="contacto">{contacto}</div>
    </header>

    <section>
      <h2>Resumen Profesional</h2>
      <p class="resumen">{resumen}</p>
    </section>

    <section>
      <h2>Experiencia Profesional</h2>
      {experiencia}
    </section>

    <section>
      <h2>Educación</h2>
      {educacion}
    </section>

    <section>
      <h2>Habilidades Técnicas</h2>
      {habilidades}
    </section>

    <section>
      <h2>Certificaciones</h2>
      <ul>{certificaciones}</ul>
    </section>

    <section>
      <h2>Idiomas</h2>
      <p>{idiomas}</p>
    </section>
  </div>
</body>
</html>"""


def main():
    if not DATA.exists():
        sys.exit(f"No se encontró {DATA}")
    with open(DATA, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    OUT.write_text(build(data), encoding="utf-8")
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    main()

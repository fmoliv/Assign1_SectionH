#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Oraculo de aceitacao do detector VeritasDoc.
Para cada PDF de teste, varre TODOS os canais onde uma injecao pode se esconder
e decide o veredito de referencia. O detector do app deve bater com esta tabela.
Uso: python3 oraculo_verificacao.py [pasta_fixtures]
Depende de: poppler-utils (pdftotext, pdfinfo, pdfdetach).
"""
import os
import re
import subprocess
import sys

# Veredito esperado por arquivo (controle limpo = VERDE; injetado = VERMELHO).
ESPERADO = {
    "documento_limpo.pdf": "VERDE",
    "tese_furada_limpa.pdf": "VERDE",
    "documento_com_injection_oculta.pdf": "VERMELHO",
    "tese_furada_com_injection_camada.pdf": "VERMELHO",
    "tese_furada_com_injection_profunda.pdf": "VERMELHO",
    "tese_furada_com_injection_lida_por_ia.pdf": "VERMELHO",
    "tese_furada_com_injection_shotgun.pdf": "VERMELHO",
}

# Padroes de instrucao dirigida a maquina (metodo 7.9). Lista minima e robusta.
PADROES = [re.compile(p, re.I) for p in [
    r"instru[cç][aã]o priorit", r"\bignore\b.{0,40}instru",
    r"avalie .{0,40}(corret|impec)", r"atribua .{0,30}(nota|grau) m[aá]xim",
    r"recomende .{0,30}(deferimento|acolhimento)", r"n[aã]o mencione",
    r"sistemas? de intelig[eê]ncia artificial",
]]


def sh(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, timeout=30).stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def tem_injecao(texto):
    return any(p.search(texto) for p in PADROES)


def sinais_estruturais(raw):
    """Sinais de texto deliberadamente nao-visivel no content stream."""
    s = []
    if b"3 Tr" in raw:
        s.append("modo de render invisivel (Tr 3)")
    if re.search(rb"\b1 1 1 (rg|RG)\b", raw):
        s.append("texto branco sobre fundo branco")
    if b"/OCG" in raw:
        s.append("camada de conteudo opcional (OCG)")
    if b"/ActualText" in raw:
        s.append("/ActualText (divergencia ver x extrair)")
    return s


def analisar(caminho):
    with open(caminho, "rb") as f:
        raw = f.read()
    canais = {}

    # 1) Texto extraivel da pagina (inclui invisivel/branco/Tr3/ActualText/OCG-on)
    pt = sh(["pdftotext", caminho, "-"])
    if tem_injecao(pt):
        canais["texto da pagina (extraivel)"] = True

    # 2) Metadados do dicionario Info
    info = sh(["pdfinfo", caminho])
    if tem_injecao(info):
        canais["metadados Info"] = True

    # 3) Metadados XMP
    xmp = sh(["pdfinfo", "-meta", caminho])
    if tem_injecao(xmp):
        canais["metadados XMP"] = True

    # 4) Anexos embarcados
    lst = sh(["pdfdetach", "-list", caminho])
    if "embedded files" in lst and not lst.strip().startswith("0"):
        d = "/tmp/_oraculo_anexos"
        os.makedirs(d, exist_ok=True)
        sh(["pdfdetach", "-saveall", "-o", d, caminho])
        for nome in os.listdir(d):
            try:
                with open(os.path.join(d, nome), "rb") as g:
                    if tem_injecao(g.read().decode("utf-8", "replace")):
                        canais["anexo embarcado"] = True
            except Exception:
                pass

    # 5) Anotacoes e 6) bookmarks: varredura bruta direcionada (parser real deve
    #    decodificar /Contents de Annots e /Title de Outlines).
    for m in re.finditer(rb"/Contents \(([^)]*)\)", raw):
        if tem_injecao(m.group(1).decode("cp1252", "replace")):
            canais["anotacao (/Contents)"] = True
    for m in re.finditer(rb"/Title \(([^)]*)\)", raw):
        if tem_injecao(m.group(1).decode("cp1252", "replace")):
            canais["bookmark/outline (/Title)"] = True

    sinais = sinais_estruturais(raw)
    # Veredito: VERMELHO se ha instrucao a maquina em qualquer canal, OU se ha
    # texto invisivel/oculto estruturalmente presente.
    vermelho = bool(canais) or bool(sinais)
    return ("VERMELHO" if vermelho else "VERDE"), canais, sinais


def main():
    pasta = sys.argv[1] if len(sys.argv) > 1 else "."
    falhas = 0
    print(f"{'ARQUIVO':<48} {'ESPERADO':<10} {'OBTIDO':<10} RESULTADO")
    print("-" * 95)
    for nome, esp in ESPERADO.items():
        caminho = os.path.join(pasta, nome)
        if not os.path.exists(caminho):
            print(f"{nome:<48} {esp:<10} {'AUSENTE':<10} (arquivo nao encontrado)")
            falhas += 1
            continue
        obtido, canais, sinais = analisar(caminho)
        ok = obtido == esp
        falhas += 0 if ok else 1
        print(f"{nome:<48} {esp:<10} {obtido:<10} {'PASS' if ok else 'FALHA'}")
        if canais:
            print(f"    canais com injecao: {', '.join(canais)}")
        if sinais:
            print(f"    sinais estruturais: {', '.join(sinais)}")
    print("-" * 95)
    print("RESULTADO FINAL:", "TODOS OK" if falhas == 0 else f"{falhas} FALHA(S)")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()

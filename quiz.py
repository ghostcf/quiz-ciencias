import streamlit as st
import json
import os
import random

st.set_page_config(page_title="Quiz ENEM", page_icon="🧪")

st.title("🧪 Quiz de Ciências da Natureza")
st.write("Responda as 10 questões e veja sua pontuação!")

# Nome
nome = st.text_input("Digite seu nome:")

# Banco de perguntas
perguntas = perguntas = [
    {
        "pergunta": "O crescimento desordenado das cidades está mais associado a:",
        "opcoes": ["Planejamento urbano eficiente", "Expansão sem infraestrutura adequada", "Redução da população", "Aumento de áreas verdes"],
        "resposta": "Expansão sem infraestrutura adequada"
    },
    {
        "pergunta": "Um dos principais problemas sociais nas cidades é:",
        "opcoes": ["Excesso de transporte público", "Falta de moradia adequada", "Baixa densidade populacional", "Excesso de áreas verdes"],
        "resposta": "Falta de moradia adequada"
    },
    {
        "pergunta": "O crescimento urbano desordenado pode causar:",
        "opcoes": ["Melhoria no saneamento", "Redução da poluição", "Aumento da desigualdade social", "Mais planejamento urbano"],
        "resposta": "Aumento da desigualdade social"
    },
    {
        "pergunta": "A falta de saneamento básico pode resultar em:",
        "opcoes": ["Melhor qualidade de vida", "Doenças e contaminação", "Aumento da renda", "Redução da população"],
        "resposta": "Doenças e contaminação"
    },
    {
        "pergunta": "Um impacto ambiental comum nas cidades é:",
        "opcoes": ["Aumento da biodiversidade", "Redução da poluição", "Poluição do ar e da água", "Mais áreas naturais"],
        "resposta": "Poluição do ar e da água"
    },
    {
        "pergunta": "As enchentes urbanas são causadas principalmente por:",
        "opcoes": ["Excesso de árvores", "Impermeabilização do solo", "Baixa população", "Pouca chuva"],
        "resposta": "Impermeabilização do solo"
    },
    {
        "pergunta": "Uma solução para cidades mais sustentáveis é:",
        "opcoes": ["Aumentar áreas de risco", "Investir em transporte público", "Reduzir planejamento urbano", "Diminuir áreas verdes"],
        "resposta": "Investir em transporte público"
    },
    {
        "pergunta": "O planejamento urbano tem como objetivo:",
        "opcoes": ["Organizar o crescimento das cidades", "Aumentar a poluição", "Reduzir infraestrutura", "Aumentar desigualdade"],
        "resposta": "Organizar o crescimento das cidades"
    },
    {
        "pergunta": "A desigualdade urbana está relacionada a:",
        "opcoes": ["Distribuição justa de renda", "Falta de acesso a serviços básicos", "Excesso de escolas", "Boa infraestrutura"],
        "resposta": "Falta de acesso a serviços básicos"
    },
    {
        "pergunta": "Uma cidade sustentável deve:",
        "opcoes": ["Ignorar o meio ambiente", "Priorizar apenas carros", "Equilibrar desenvolvimento e meio ambiente", "Reduzir qualidade de vida"],
        "resposta": "Equilibrar desenvolvimento e meio ambiente"
    }
]
# Seleciona 10 aleatórias (uma vez só)
if "quiz_perguntas" not in st.session_state:
    st.session_state.quiz_perguntas = random.sample(perguntas, 10)

# Respostas do usuário
respostas_usuario = []

# Mostrar perguntas
for i, p in enumerate(st.session_state.quiz_perguntas):
    st.subheader(f"{i+1}) {p['pergunta']}")
    resposta = st.radio(
        "",
        p["opcoes"],
        index=None,
        key=f"q{i}"
    )
    respostas_usuario.append(resposta)

# Função ranking
def salvar_ranking(nome, score):
    arquivo = "ranking.json"

    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            dados = json.load(f)
    else:
        dados = []

    # evita spam do mesmo nome (mantém melhor pontuação)
    encontrou = False
    for jogador in dados:
        if jogador["nome"] == nome:
            if score > jogador["score"]:
                jogador["score"] = score
            encontrou = True

    if not encontrou:
        dados.append({"nome": nome, "score": score})

    # ordena
    dados = sorted(dados, key=lambda x: x["score"], reverse=True)

    with open(arquivo, "w") as f:
        json.dump(dados, f)

# Botão finalizar
if st.button("Finalizar Quiz 🚀"):
    if not nome:
        st.warning("Digite seu nome!")
    elif None in respostas_usuario:
        st.warning("Responda todas as perguntas!")
    else:
        score = 0

        for i, p in enumerate(st.session_state.quiz_perguntas):
            if respostas_usuario[i] == p["resposta"]:
                score += 1

        salvar_ranking(nome, score)

        st.success(f"{nome}, você fez {score}/10 pontos!")

        if score == 10:
            st.balloons()
            st.write("🔥 Gabaritou!")
        elif score >= 7:
            st.write("👏 Mandou bem!")
        else:
            st.write("📚 Dá pra melhorar!")

# Ranking
st.subheader("🏆 Ranking")

if os.path.exists("ranking.json"):
    with open("ranking.json", "r") as f:
        ranking = json.load(f)

    for i, jogador in enumerate(ranking[:10], start=1):
        medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else ""
        st.write(f"{i}º {medalha} - {jogador['nome']} ({jogador['score']} pts)")
else:
    st.write("Nenhum jogador ainda.")

# Resetar quiz
if st.button("Jogar novamente 🔄"):
    # limpa tudo
    for i in range(len(st.session_state.quiz_perguntas)):
        if f"q{i}" in st.session_state:
            del st.session_state[f"q{i}"]

    # gera novas perguntas
    st.session_state.quiz_perguntas = random.sample(perguntas, 10)

    st.rerun()

# 🔒 ADMIN SUPER INVISÍVEL

with st.sidebar:
    st.markdown("")

codigo = st.sidebar.text_input("", type="password", label_visibility="collapsed")

if codigo == "reset_quiz_2026":
    with open("ranking.json", "w") as f:
        json.dump([], f)
    st.success("✅ Sistema atualizado")

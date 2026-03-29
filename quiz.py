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
perguntas = [
    {"pergunta": "Unidade da corrente elétrica?", "opcoes": ["Volt", "Ampere", "Ohm", "Watt"], "resposta": "Ampere"},
    {"pergunta": "O DNA armazena?", "opcoes": ["Energia", "Informação genética", "Proteínas", "Oxigênio"], "resposta": "Informação genética"},
    {"pergunta": "Lei de Ohm: V = R . ?", "opcoes": ["Potência", "Corrente", "Energia", "Carga"], "resposta": "Corrente"},
    {"pergunta": "Planeta mais próximo do Sol?", "opcoes": ["Terra", "Marte", "Mercúrio", "Vênus"], "resposta": "Mercúrio"},
    {"pergunta": "Fórmula da água?", "opcoes": ["CO2", "H2O", "O2", "H2"], "resposta": "H2O"},
    {"pergunta": "Órgão responsável pela respiração?", "opcoes": ["Coração", "Pulmão", "Fígado", "Rim"], "resposta": "Pulmão"},
    {"pergunta": "Velocidade da luz é aproximadamente?", "opcoes": ["300 mil km/s", "150 mil km/s", "1 milhão km/s", "30 mil km/s"], "resposta": "300 mil km/s"},
    {"pergunta": "pH menor que 7 é?", "opcoes": ["Básico", "Neutro", "Ácido", "Alcalino"], "resposta": "Ácido"},
    {"pergunta": "Gás essencial para respiração?", "opcoes": ["CO2", "O2", "N2", "H2"], "resposta": "O2"},
    {"pergunta": "Função das mitocôndrias?", "opcoes": ["Digestão", "Produzir energia", "Respiração externa", "Transporte"], "resposta": "Produzir energia"},
    {"pergunta": "Unidade de força?", "opcoes": ["Joule", "Newton", "Watt", "Pascal"], "resposta": "Newton"},
    {"pergunta": "Ecossistema é?", "opcoes": ["Só animais", "Só plantas", "Seres vivos + ambiente", "Só água"], "resposta": "Seres vivos + ambiente"}
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
    st.session_state.clear()
    st.rerun()
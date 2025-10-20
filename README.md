# 🎧 YTGrabber: A Ferramenta Suprema de Linha de Comando para YouTube

<div align="center">

![GitHub release](https://img.shields.io/github/v/release/JoaoDEVWHADS/YTGrabber?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/JoaoDEVWHADS/YTGrabber?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/JoaoDEVWHADS/YTGrabber?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/JoaoDEVWHADS/YTGrabber?style=for-the-badge)

**Uma solução completa, leve e poderosa para buscar, reproduzir e baixar conteúdo de Áudio e Vídeo do YouTube e YouTube Music diretamente pelo seu Terminal.**

[📦 Versão Compilada](#-versão-compilada-executável-pronto) •
[💻 Instalação (Código Fonte)](#-instalação-a-partir-do-código-fonte) •
[✨ O Poder dos Recursos](#-o-poder-dos-recursos) •
[🚀 Guia de Uso Rápido](#-guia-de-uso-rápido) •
[🐛 Reportar Bug/Sugestão](https://github.com/JoaoDEVWHADS/YTGrabber/issues)

</div>

---

## 🌍 Onde Mais Me Encontrar?

*Se precisar ler isso em outro idioma, confira as versões abaixo:*

- **Português (Brasil)** - *Você está aqui*
- [English](README.en.md)
- [Español](README.es.md)
- [Português (Portugal)](README.ptpt.md)

---

## 📖 A Missão do Projeto (Por que o YTGrabber Existe?)

Maluco, o **YTGrabber** nasceu da necessidade de ter um controle total e sem frescura sobre o conteúdo do YouTube e YouTube Music. Chega de interface gráfica pesada, de sites de terceiros cheios de anúncio ou de serviços duvidosos.

Desenvolvida em **Python**, esta ferramenta de linha de comando (CLI) é a pedida para quem quer **eficiência, velocidade e privacidade**. Ela te permite não só baixar vídeos e músicas, mas também organizá-los automaticamente, reproduzir o conteúdo antes de baixar (graças ao MPV player integrado) e garantir que todo áudio seja convertido para o formato universal: **MP3**.

É a ferramenta ideal para desenvolvedores, sysadmins e qualquer pessoa que prefira a agilidade do terminal e a certeza de que seus downloads de áudio e vídeo estão sendo feitos de forma local e segura.

---

## ✨ O Poder dos Recursos (O que o YTGrabber Faz?)

Presta atenção nesse arsenal, truta:

| Categoria | Recurso Detalhado | Descrição e Vantagem |
|---|---|---|
| **Busca e Navegação** | **🔍 Busca Integrada e Organizada** | Pesquisa direta no YouTube e YouTube Music. Os resultados são apresentados de forma clara e numerada no terminal, facilitando a escolha. |
| | **▶️ Reprodução Instantânea (MPV)** | Não precisa baixar pra saber se é o que você queria! Use o MPV Player embutido para pré-visualizar vídeos ou ouvir músicas *direto do terminal* antes de iniciar o download. |
| **Download** | **💾 Download de Áudio em MP3** | Foco total em áudio! O programa garante o download e a conversão automática do arquivo para **MP3** utilizando o poder do **FFmpeg**, com a melhor qualidade disponível. |
| | **📦 Suporte a Downloads em Massa** | Baixe tudo de uma vez! Suporta o download completo de **Playlists, Álbuns (do YouTube Music)** e até mesmo **Canais** inteiros com apenas um comando. |
| | **🍪 Acesso a Conteúdo Restrito** | Possui um sistema para importar **cookies** de navegação, permitindo que você acesse e baixe conteúdo restrito ou privado (como músicas do YouTube Music que exigem login). |
| **Usabilidade** | **🇧🇷 Interface 100% em Português** | Totalmente amigável para o usuário brasileiro, com menus intuitivos e mensagens claras. Não precisa se virar no "inglês técnico"! |
| | **📁 Organização Inteligente de Pastas** | Seus downloads não vão virar uma bagunça. O YTGrabber organiza automaticamente os arquivos em pastas separadas (`downloads/`, `playlists/`, `albuns/`, `canais/`), baseadas no tipo de conteúdo baixado. |
| **Performance e Segurança** | **⚡ Leve e Veloz (CLI)** | Por ser uma interface de linha de comando (CLI), o consumo de recursos é mínimo, garantindo velocidade e estabilidade, mesmo em máquinas mais antigas. |
| | **🔒 Privacidade Total (Local)** | Segurança em primeiro lugar! Tudo, desde a busca até o download e conversão, roda **localmente** na sua máquina. Seus dados e seu uso não são enviados para terceiros. |

---

## 📦 Versão Compilada (Executável Pronto)

**Quer pular a instalação do Python, Git e dependências?**

Se a sua intenção é apenas usar o programa rapidinho no **Windows**, a versão compilada é a sua praia!

Acesse a página de **[Releases](https://github.com/JoaoDEVWHADS/YTGrabber/releases/latest)** no GitHub para:

1.  Baixar o **executável (.exe)** pronto para usar.
2.  Ver a descrição detalhada de cada versão.
3.  Conferir os requisitos e instruções de uso específicas para o executável.

**Se você adora programar (como eu sei que tu adora Node.JS, PHP, Python, maluco!) e prefere rodar o projeto direto do código fonte, prossiga com as instruções detalhadas abaixo! 👇**

---

## 💻 Instalação a Partir do Código Fonte

Para rodar o YTGrabber a partir do código fonte, garantindo a máxima flexibilidade e customização, siga os passos abaixo.

### ⚙️ Pré-requisitos Fundamentais

Antes de tudo, você precisa garantir que tem o seguinte instalado no seu sistema:

1.  **Python 3.11 ou superior:** É a linguagem em que o projeto foi escrito. É **altamente recomendável** usar a versão 3.11+ para evitar problemas de compatibilidade com as bibliotecas.
2.  **Git:** (Opcional, mas recomendado) Ferramenta para clonar o repositório de forma fácil e manter o código atualizado.
3.  **Bibliotecas Externas (FFmpeg e MPV):** Essas são as ferramentas de *baixo nível* que o YTGrabber usa para fazer a mágica acontecer. **Veja as instruções de instalação para elas na próxima seção!**

---

### 📥 Passo 1: Obter o Código Fonte (Duas Opções)

Você pode baixar o código-fonte da maneira que achar mais fácil, truta:

#### Opção A: Clonar com Git (Recomendado para Devs)

Essa é a maneira mais limpa e ideal para quem quer contribuir ou apenas manter o projeto atualizado facilmente.

```bash
# 1. Abre teu terminal em um diretório de projetos
cd ~/Projetos/

# 2. Clona o repositório do YTGrabber
git clone [https://github.com/JoaoDEVWHADS/YTGrabber.git](https://github.com/JoaoDEVWHADS/YTGrabber.git)

# 3. Entra na pasta do projeto recém-clonado
cd YTGrabber
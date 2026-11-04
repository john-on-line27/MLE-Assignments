# Recommended Setup

**Any development environment will do.** If you already have an editor you like, keep using it. If you already have an AI subscription that comes with a coding agent, using that is probably a bit more fruitful, and certainly more relaxed. The free setup below works, but it's a little limited: KISSKI, the AI service it uses, limits how many requests you can make (at the time of writing, 10 per minute, 200 per hour and 400 per day). A coding agent can make several requests for a single question, so you may hit these limits on a busy day.

This page is for you if you don't have a setup yet, or aren't happy with the one you have.


## Text Editor: Zed

We recommend [Zed](https://zed.dev/). It's free, fast and light on your computer's resources, and it runs on macOS, Linux and Windows.

Python support works out of the box. Zed comes with a Python language server (basedpyright), which knows Python, NumPy and PyTorch. It gives you:

- completions as you type, including function arguments,
- the documentation of a function or class when you hover over it,
- jumping to where something is defined,
- warnings about type errors and other mistakes before you run the code.

To get started, open an assignment's folder in Zed after you've run `make install`. Zed should find the assignment's virtual environment (`.venv/`) by itself, and that's what lets it know about NumPy and PyTorch. If completions for these libraries don't show up, see [Zed's Python guide](https://zed.dev/docs/languages/python).

**Windows users:** keep your assignments inside WSL, and open them from there.

Zed doesn't work for you? [VS Code](https://code.visualstudio.com/) with its Python extension is the most common alternative. It's heavier, but you'll find help for it everywhere.


## Coding Agent: Kilo Code

We recommend [Kilo Code](https://kilo.ai/) as the coding agent. It's free and open source, and it runs in a terminal, so it works next to any editor. Zed has a terminal built in, so you can keep everything in one window.

Install it with Kilo's install script:

```bash
curl -fsSL https://kilo.ai/cli/install | bash
```

The script downloads Kilo for your system into `~/.kilo/bin/` and adds that folder to your `PATH`, so open a new terminal afterwards. Check that it worked with `kilo --version`. If you already use [Node.js](https://nodejs.org/), `npm install -g @kilocode/cli` installs the same thing.

Then go into an assignment's folder and start it:

```bash
cd <assignment-folder>
kilo
```

Always start it inside the assignment's folder. That's where it finds `AGENTS.md`.

Kilo Code is only the harness, the program that runs the agent. It still needs a model to talk to, which comes from a provider.


## Model Provider: KISSKI

[KISSKI](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/) is an AI service for German universities, run by the GWDG. Students get access through their university account, free of charge.

1. Log in to [Academic Cloud](https://academiccloud.de/) with your university account. On the initial login page, click "Federated Login" and select TU Berlin (or whatever uni you have a log-in for). This should bring you to a familiar TU Berlin login page where you can enter your credentials (no "@tu-berlin.de)
2. Try going to [SAIA website ](https://saia.gwdg.de/), it you're not logged in there, do so, and click on "API keys" in the lower left corner. You should be able to request an API key from this page.
3. If step 2 doesn't work, request an API key on the [KISSKI LLM service page](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/). To start, click the "Book" button on the upper right (It has an arrow pointing to the right). Use the same email address as your Academic Cloud account.
4. Save your key in an environment variable. Add this line to your `~/.bashrc` (or `~/.zshrc` on macOS), then open a new terminal:

   ```bash
   export KISSKI_API_KEY="<your-api-key>"
   ```

5. Copy our Kilo settings for KISSKI, [`kilo.jsonc`](kilo.jsonc), into Kilo's settings folder:

   ```bash
   mkdir -p ~/.config/kilo
   cp kilo.jsonc ~/.config/kilo/kilo.jsonc
   ```

   Run this from the `docs/` folder. If you already have a `~/.config/kilo/kilo.jsonc`, copy the parts you need into it instead.

6. Start `kilo` in an assignment's folder. It starts with GLM 5.3 Flash, which is good at coding and at working as an agent. Type `/models` to switch to one of the others in the settings.

Don't share your API key with anyone, and never commit it to Git.


## Chat Assistant: Lumo

For assignments that also work with a chat assistant in your browser, we recommend [Lumo](https://lumo.proton.me/) by Proton. It's privacy-focused: Proton doesn't use your chats to train its models. You can try it without an account, and a free Proton account gives you more questions per week.

Remember to paste `AGENTS.md` into the chat, or attach it, before you start.

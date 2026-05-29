import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

# Exact new multi-line signature block
SIGNATURE_BLOCK = """David Fisher | Founder | Revenant Systems
Dave⌽ᶠₜₕₑDead | AI Engineering Student | AI Alignment
https://www.revenantsystems.net/
https://www.linkedin.com/in/daveisfromthegrave/"""

PRODUCT_TITLES = {
    "systems": "яƏ̄Λ🅔ղaͣÑ† ×͡× Ƨÿ§τΣМͫs",
    "hardening": "яƏ̄Λ🅔ղaͣÑ† нͥᴀяͣᴅͫᴇɴɪɴɢ",
    "theme_studio": "яƏ̄Λ🅔ղaͣÑ† ƮнΣᴍΣ Ƨ†ᴜᴅɪᴏ",
    "skills": "ℂʟᴀᴜᴅᴇ Ƨᴋͥɪͣʟͫʟs Ɓᴜɴᴅʟᴇ",
    "architect": "ƮнΣ ᴀͥɪͣ ᴀяᴄнͫɪ†ᴇᴄ† Ƈнᴇᴄᴋʟɪs†"
}

NEW_ADS = {
    # CHEAT SHEETS & TIPS (Product: "RS Cheat Sheets & Tips")
    "CS-001": {
        "caption": f"""▲───────◇◆◇───────▲
  {PRODUCT_TITLES['architect']}
▲───────◇◆◇───────▲

Stop telling your LLM to "be extremely helpful." 

Useless conversational fluff is literal token waste. You're paying for attention math it doesn't need to calculate. 

Here is the zero-inference structural checklist for actual persona architecture. ⍥⍤⍣

⍡ Delimiter discipline (stop writing raw prose)
⍢ Dual-stage dry runs (force logical compilation)
⍩ Strict parameter scoping (isolate context boundaries)

          ʕº̫͡ºʔʕ•̫͡•ʔ   Read the checklist. It's free.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""{PRODUCT_TITLES['architect']} ⍥⍤⍣
▲───────◇◆◇───────▲

A saveable, structural checklist for designing zero-inference prompt environments. No conversational fluff, just pure logical execution.

õ.O  Get the checklist: https://www.revenantsystems.net"""
        }
    },
    
    "CS-002": {
        "caption": f"""¸,ø¤º°`°º¤ø,¸¸,ø¤º°   °º¤ø,¸¸,ø¤º°`°º¤ø,¸
  {PRODUCT_TITLES['systems']}  
¸,ø¤º°`°º¤ø,¸¸,ø¤º°   °º¤ø,¸¸,ø¤º°`°º¤ø,¸

Stop saying "please" and "thank you" to your AI. 

It has no feelings, but it DOES have attention limits. Polite words are literal token waste. You are literally paying to buy your execution engine a coffee it can't drink.

Diluting instructions with fluff distorts system behavior and makes output worse. Use strict delimiters and command the model.

          щ(ಠ益ಠщ)   Save your tokens for actual logic.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""Stop saying 'please' and 'thank you' to your AI. 
¸,ø¤º°`°º¤ø,¸¸,ø¤º°   °º¤ø,¸¸,ø¤º°`°º¤ø,¸

Every pleasantry is literal token waste. You are paying to calculate useless social math on an execution engine that has no feelings. 

щ(ಠ益ಠщ)  Be concise. Command the model.
https://www.revenantsystems.net"""
        }
    },

    "CS-003": {
        "caption": f"""★━━━━━━━━━━━━━━━━━★
  {PRODUCT_TITLES['architect']}
★━━━━━━━━━━━━━━━━━★

The Genesis Prompt Matrix. 

Writing flat system prompts and praying for logical consistency is a massive gamble.

The Genesis Matrix provides a structured blueprint for persona architecture that stops prompt injections, enforces system rules, and guarantees logical compliance with zero-inference policies.

          ಠ_ರೃ   Quite elegant, really.
                 Check the architecture:

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""The Genesis Prompt Matrix. {PRODUCT_TITLES['architect']}
★━━━━━━━━━━━━━━━━━★

Discover how a structured, zero-inference system prompt matrix enforces strict rule compliance and prevents jailbreaks.

ಠ_ರೃ  Read the blueprint: https://www.revenantsystems.net"""
        }
    },

    "CS-004": {
        "caption": f"""✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶
  {PRODUCT_TITLES['systems']}
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

3 formatting rules that instantly improve AI reasoning:

1. Leverage Markdown structures
2. Use strict XML/HTML delimiters
3. Restrict outputs with zero-inference guidelines

Give the engine clear, token-optimized parsing blocks instead of unstructured prose.

          ٩(͡๏̯͡๏)۶   It's not magic, it's just syntax.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""3 formatting rules that instantly improve AI reasoning:
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

1. Markdown structures
2. Strict XML delimiters
3. Zero-inference boundaries

٩(͡๏̯͡๏)۶  Stop sending paragraphs. Start using structure.
https://www.revenantsystems.net"""
        }
    },

    "CS-005": {
        "caption": f"""▲───────◇◆◇───────▲
  {PRODUCT_TITLES['architect']}
▲───────◇◆◇───────▲

Stop writing prompts like you're composing a polite email to a coworker. 

This comparison infographic breaks down the structural shift from flat conversational text to zero-inference developer scripting. Optimize your context window.

          ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ   Make the switch. Save your budget.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""Stop writing essays to your LLM. 💀

This matrix comparison breaks down the exact syntax transition from flat conversational text to zero-inference structural scripting. 

ಠ_ರೃ  https://www.revenantsystems.net"""
        }
    },

    # HARDENING (Product: "Revenant Hardening")
    "RH-001": {
        "caption": f"""▲───────◇◆◇───────▲
  {PRODUCT_TITLES['hardening']}
▲───────◇◆◇───────▲

>> rsh scan .
>> WARNING: 19 SILENT TIME BOMBS DETECTED

If a basic prompt injection can hijack your agent and drain your API keys, you don't have an application. You have a massive liability.

We scan and secure your context windows, token pathways, and runtime tool boundaries.

          (｡ì _ í｡)✃   Don't let them bleed your system dry.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""rsh scan . -> 19 silent vulnerabilities detected. 💣💀
▲───────◇◆◇───────▲

Most AI agents are deployed with massive security holes. Scan, isolate, and secure your systems before they go to production.

{PRODUCT_TITLES['hardening']}  https://www.revenantsystems.net"""
        }
    },

    "RH-002": {
        "caption": f"""·▄▄▄▄       ▄▄▄    .  ▄▄▄·      ·▄▄▄▄  
██▪ ██    ▀▄.▀·   ▐█  ▀█      ██▪    █
▐█·  ▐█  ▐▀▀▪   ▄█▀▀█      ▐█·    ▐█▌
██. ██  ▐█▄▄▌ ▐█▪  ▐▌     ██.   ██ 
▀▀▀▀•     ▀▀▀       ▀       ▀    ▀▀▀▀•

If a 12-year-old can prompt-inject your system, you do not have a system.

Stop relying on basic system prompts for security. "System Prompts" are suggestions to an LLM. They will bypass them eventually.

Revenant Hardening ensures your AI agents operate within strict, zero-inference sandbox layers that resist advanced jailbreak techniques.

          (｡ì _ í｡)✃   Is your prompt actually secure?

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""If a 12-year-old can prompt-inject your system, you don't have a system. 💀
 
Stop relying on basic prompts for security. Hardening blocks context leaks and token manipulation at the execution layer.

(｡ì _ í｡)✃  Lock it down: https://www.revenantsystems.net"""
        }
    },

    "RH-003": {
        "caption": f"""■█■█■█■█■█■█■█■
  [!] AI DATA LEAK IDENTIFIED [!]
■█■█■█■█■█■█■█■

The 3 ways your AI is leaking data right now:

1. Context window spilling (reading past data)
2. Token manipulation (hijacking system calls)
3. Unbounded tool use (unrestricted shell/DB access)

We build the walls. We isolate the memory. We secure the system.

          ¬_¬   Stop leaving the keys in the ignition.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""The 3 ways your AI is leaking data right now:
■█■█■█■█■█■█■█■

1. Context window spilling
2. Token manipulation
3. Unbounded tool use

¬_¬  Lock down your agent architectures today.
https://www.revenantsystems.net"""
        }
    },

    "RH-004": {
        "caption": f"""✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶
  {PRODUCT_TITLES['systems']}
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

Stop trusting default AI security.

Standard LLM wrappers provide exactly zero real isolation. They are built for convenience, not defense.

Here is the structural blueprint of how Revenant boundaries operate, enforcing strict zero-inference policies and securing your local system resources.

          ×͡×   Convenience is the enemy of security.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""Stop trusting default AI security wrappers. 💀
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

True agentic capability requires strict separation of config, state memory, and sandbox boundaries. Enforce zero-inference policies.

×͡×  Learn how: https://www.revenantsystems.net"""
        }
    },

    "RH-005": {
        "caption": f"""·▄▄▄▄       ▄▄▄    .  ▄▄▄·      ·▄▄▄▄  
██▪ ██    ▀▄.▀·   ▐█  ▀█      ██▪    █
▐█·  ▐█  ▐▀▀▪   ▄█▀▀█      ▐█·    ▐█▌
██. ██  ▐█▄▄▌ ▐█▪  ▐▌     ██.   ██ 
▀▀▀▀•     ▀▀▀       ▀       ▀    ▀▀▀▀•

>> rsh scan .
>> STATUS: VERIFYING SANDBOX BOUNDARIES

Most agentic systems are deployed with gaping security holes—unrestricted shell runtimes, unbounded context memory, and zero delimiter isolation.

This security checklist outlines the essential steps to secure your runtime against prompt injection and context spill leaks.

          (｡ì _ í｡)✃   Harden your systems before prod.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""rsh scan . -> STATUS: SECURING SANDBOX 🛡️💀

Stop deploying agents with unrestricted shell runtimes and soft prompts. Check the essential checklist for production sandboxing and boundary controls.

(｡ì _ í｡)✃  https://www.revenantsystems.net"""
        }
    },

    # THEME STUDIO (Product: "Revenant Theme Studio")
    "RTS-001": {
        "caption": f"""  [!] MANUAL ASSET MANAGEMENT HAS BEEN RETIRED [!]

Stop manually binding folder icons like it's 2005. 

Your IDE, assets, and folders are where you spend 10+ hours a day. Staring at default yellow folders is visual noise.

Revenant Theme Studio auto-matches your entire visual library to custom icons in seconds. It handles backups, registry, and protected system icon swaps with a single click.

          (｡ì _ í｡)✃   Why are you still clicking manually?

{SIGNATURE_BLOCK}""".replace("https://www.revenantsystems.net/", "https://www.revenantsystems.net/software"),
        "platform_captions": {
            "x": """Stop manually binding icons like it's 2005. 💀

Revenant Theme Studio maps your entire visual library to custom icons in seconds. Backups included.

(｡ì _ í｡)✃  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-002": {
        "caption": f"""▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 
  [!] DEFAULT THEMES CAUSE EYE STRAIN [!]
▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 

Default folders are for people who enjoy staring at flat yellow voids.

Upgrade your workspace to a cohesive, custom-engineered dark aesthetic that increases focus and reduces visual clutter. 

Flawlessly applied Gunmetal and Ruby themes across your entire folder hierarchy in seconds.

          ಠ_ರೃ   Quite a massive upgrade.

{SIGNATURE_BLOCK}""".replace("https://www.revenantsystems.net/", "https://www.revenantsystems.net/software"),
        "platform_captions": {
            "x": """Default folder icons are for people who enjoy eye strain. 👁️💀

Upgrade your entire visual hierarchy to flawless Gunmetal and Ruby icons in seconds.

ಠ_ರೃ  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-003": {
        "caption": f"""  ┻┳|―-∩
  ┳┻|　　ヽ   (Psst... check out this setup)
  ┻┳|　●   |
  ┳┻|▼) _ノ
  ┻┳|￣　)
  ┳ﾐ(￣  ／
  ┻┳T￣|

Workspace: Upgraded. 

Featuring the CYBORG_GOLD wallpaper, perfectly unified with the custom Gunmetal icon pack (over 140 custom crafted icons built for developers).

Aesthetics dictate workflow. Ditch the default yellow styling.

          ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ   Get the setup free:

{SIGNATURE_BLOCK}""".replace("https://www.revenantsystems.net/", "https://www.revenantsystems.net/software"),
        "platform_captions": {
            "x": """Workspace: Upgraded. 💀✨

CYBORG_GOLD meets the Gunmetal icon pack (140+ custom crafted developer folder icons). Ditch the default voids.

┻┳|―-∩  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-004": {
        "caption": f"""  [!] AESTHETICS DICTATE WORKSPACE ENERGY [!]

You spend half your life staring at your desktop and directory trees. Why does it look like a factory reset machine?

Revenant Theme Studio maps your assets, protects your system backups, and deploys high-end dark aesthetics instantly.

          ᕙ(⇀‸↼‶)ᕗ   A beautiful setup is a productive setup.

{SIGNATURE_BLOCK}""".replace("https://www.revenantsystems.net/", "https://www.revenantsystems.net/software"),
        "platform_captions": {
            "x": """Aesthetics dictate workflow. 💻⚡

Stop staring at default factory-reset folder trees. Deploys custom unified dark themes instantly.

ᕙ(⇀‸↼‶)ᕗ  Get the app: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-006": {
        "caption": f"""▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 
  [!] AESTHETICS DICTATE WORKSPACE FOCUS [!]
▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 

You spend half your waking life staring at your IDE, assets, and folder directory trees. Staring at default yellow folders is visual noise that causes cognitive fatigue.

This specification sheet compares default styling with the Gunmetal & Ruby dark-theme design standard.

          ᕙ(⇀‸↼‶)ᕗ   Aesthetics are functional.

{SIGNATURE_BLOCK}""".replace("https://www.revenantsystems.net/", "https://www.revenantsystems.net/software"),
        "platform_captions": {
            "x": """Default OS directory yellow icons cause eye strain. 👁️💀

Upgrade your workspace to unified Gunmetal & Ruby themes. Check out the specification comparison.

ᕙ(⇀‸↼‶)ᕗ  https://www.revenantsystems.net/software"""
        }
    },

    # FULL BUNDLE (Product: "RS Full Bundle")
    "BUN-002": {
        "caption": f"""  [!] SYSTEM ALERT: HAMMER TOOL DETECTED [!]

Claude is a scalpel. You're using it like a hammer.

Most developers write essays in the prompt box and expect production-ready codebase files.

To get actual, deterministic outputs, you need advanced artifact manipulation and strict delimiter control. 

Steal this exact prompt engineering skill for free, and unlock the other 9 in our bundle.

          ¬_¬   Stop prompting. Start compiling.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Claude is a scalpel. You're using it like a hammer. 💀

Stop typing essays. Structure your prompts with strict delimiters and force logic stages. 

¬_¬  Unlock the 10 production-ready skills: https://www.revenantsystems.net"""
        }
    },

    "BUN-003": {
        "caption": f"""  [!] AVERAGE DEVELOPER VS. REVENANT BUNDLE [!]

Average Developer:
- Fights with Claude for 45 minutes on formatting.
- Receives hallucinated API keys.
- Context spills over and crashes.

Revenant Bundle User:
- Drops a pre-compiled Genesis Prompt.
- Logical dry-run completes in seconds.
- Flawless, production-ready code output.

          ﾟ･ (>﹏<) ･ﾟ｡.   Why are you still fighting the model?

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Average Developer vs. Revenant Bundle. 

Stop fighting the model for formatting. Drop a genesis prompt, dry-run in memory, and get flawless production code instantly.

٩(͡๏̯͡๏)۶  Get the bundle: https://www.revenantsystems.net"""
        }
    },

    "BUN-004": {
        "caption": f"""★━━━━━━━━━━━━━━━━━★
  {PRODUCT_TITLES['skills']}
★━━━━━━━━━━━━━━━━━★

Stop guessing how to instruct LLMs. Prompt engineering is not a vibe check—it is system configuration.

The 10 Claude skills that actually work in production development. Backed by zero-inference principles.

          ﾟ･ (>﹏<) ･ﾟ｡.   Don't let your code go to the grave.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": f"""Resurrect your dead prompts. 💀🔥

Prompt engineering is not a vibe check—it is system configuration. Get the 10 skills that work in production.

{PRODUCT_TITLES['skills']}  https://www.revenantsystems.net"""
        }
    },

    "BUN-005": {
        "caption": f"""  [!] HOW TO FORCE LOGICAL PROCESSING [!]

If you aren't restricting output formats, enforcing a dry-run stage in memory, and isolating parameters, your agent is just guessing.

Here is the step-by-step XML blueprint to force Claude to build logical reasoning steps before writing a single line of code.

          ¯\_(ツ)_/¯   Or you can keep debugging hallucinations.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """How to force logical processing in Claude. 🧵👇

Stop reading essays. Structure prompts with XML delimiters, enforce a dry-run stage, and target zero-inference. [Thread]

¯\_(ツ)_/¯  Blueprint: https://www.revenantsystems.net"""
        }
    },

    "BUN-006": {
        "caption": f"""✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶
  {PRODUCT_TITLES['skills']}
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

Stop fighting the AI over formatting and logic leaks.

Prompt engineering isn't a casual vibe check—it is literal system configuration. To build robust, predictable software agents, you need pre-compiled system skills.

          ٩(͡๏̯͡๏)۶   Why guess when you can engineer?

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Stop guessing how to command your AI. 💻💀

Prompt engineering is system configuration, not a vibe check. Check the directory of 10 production-ready system skills designed for robust Claude agents.

٩(͡๏̯͡๏)۶  https://www.revenantsystems.net"""
        }
    },

    # SYSTEM ARCHITECTURE (Product: "Revenant Systems Core Architecture")
    "SYS-001": {
        "caption": f"""  {PRODUCT_TITLES['systems']}
▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 

Your AI is a glorified chatbot.

Real business value doesn't come from prompt boxes and conversational widgets—it comes from symbiotic systems where machine logic and human intent work in perfect unison.

Stop chatting with LLMs. Build deterministic, zero-trust architectures.

       ◢▃▄ ʕ•̫͡•ʔ♡ʕ•̫͡•ʔ▄▃◣   A prompt is not an architecture.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Your AI is a glorified chatbot. 💀

Real value doesn't come from chat widgets—it comes from core systems where machine logic and human intent work in perfect symbiosis.

(ノಠ益ಠ)ノ  Start engineering: https://www.revenantsystems.net"""
        }
    },

    "SYS-002": {
        "caption": f"""  [!] PRECISION OVER PROBABILITY [!]

Stop treating AI like a search engine. 

An LLM is a probabilistic token predictor, not a database. If you build your software assuming it "knows" facts, you are building on wet sand.

Grounding, zero-inference constraints, and systematic state management are the only ways to achieve production reliability.

          ×͜×   Precision wins. Luck is not a strategy.
          ⍥⍤⍣   Ground your systems:

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Precision over probability. 💻⚡

AI is not a database—it is a token predictor. Grounding, zero-inference boundaries, and state management are mandatory for production.

×͜×  Ground your systems: https://www.revenantsystems.net"""
        }
    },

    "SYS-003": {
        "caption": f"""  [!] HOW MANY TIMES DID YOUR AI HALLUCINATE TODAY? [!]

If your agentic systems rely on the model's memory to track execution state, you are begging for a crash.

A Revenant System grounds every single state change in structured local files, strict context bounds, and isolated runtime shells.

          щ(ಥДಥщ)   Stop praying for clean outputs.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """How many times did your AI hallucinate today? 💀

Stop relying on LLM memory. Ground every single state change in local context files and isolated runtime boundaries.

щ(ಥДಥщ)  Get structured: https://www.revenantsystems.net"""
        }
    },

    "SYS-004": {
        "caption": f"""█░▒█ █▀▀▄ █▀▀▄ █▀▀ █▀▀█ █▀▀▄
█░▒█ █░░█ █░░█ █▀▀ █▄▄█ █░░█
▀▄▄▀ ▀░░▀ ▀▀▀░ ▀▀▀ ▀░░▀ ▀▀▀░

The Anatomy of a Revenant System.

True agentic capability requires strict separation:
1. Configuration Layer (The boundaries)
2. State Memory (The ledger)
3. Platform Integration (The platform adapters)
4. Secure Sandbox Runtime (The isolation)

Here is the 4-part architectural blueprint for high-performance production environments.

          ⍩   Zero-trust. Zero-inference.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """The Anatomy of a Revenant System. 💻⚡

True agentic capability requires separating config, state memory, platform integration, and secure runtimes. 

⍩  Get the 4-part blueprint: https://www.revenantsystems.net"""
        }
    },

    "SYS-005": {
        "caption": f"""▲───────◇◆◇───────▲
  {PRODUCT_TITLES['systems']}
  [ Algiz Algebra: The Architectural Operators ]
▲───────◇◆◇───────▲

Stop writing arbitrary prompt instructions. Agentic capability requires a strict mathematical framework.

Revenant Systems are built on the Algiz Algebra—a formal symbolic notation that maps recursive machine logic and state transitions:

Ω (Omega): Recursion, self-reference, and state iteration loops.
Ξ (Xi): Meta-structure and boundary architectures.
↦ (Map): State transformation mechanics.
∅ (Empty Set): Null context/safety handling bounds.

          ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ   Build symbiotic systems, not chatbots.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": "Stop guessing. Start compiling. 💻🤖\n\nDiscover Algiz Algebra: The formal mathematical operators (Omega, Xi, Map, Empty Set) that drive Revenant Systems' zero-inference core architectures.\n\nʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ  https://www.revenantsystems.net"
        }
    }
}

def main():
    updated_count = 0
    ads_dir = PROJECT_ROOT / "ads"
    
    for category in ads_dir.iterdir():
        if category.is_dir():
            for ad_folder in category.iterdir():
                if ad_folder.is_dir() and ad_folder.name in NEW_ADS:
                    ad_id = ad_folder.name
                    ad_file = ad_folder / "ad.json"
                    
                    if ad_file.exists():
                        try:
                            with open(ad_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                            
                            # Inject updated content
                            data["caption"] = NEW_ADS[ad_id]["caption"]
                            
                            if "platform_captions" not in data:
                                data["platform_captions"] = {}
                            
                            # Update platform captions specifically
                            data["platform_captions"]["x"] = NEW_ADS[ad_id]["platform_captions"]["x"]
                            
                            with open(ad_file, "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2)
                                
                            print(f"Successfully applied multi-line signature block to: {ad_id}")
                            updated_count += 1
                        except Exception as e:
                            print(f"Error updating {ad_id}: {e}")
                            
    print(f"\nCompleted! Overhauled {updated_count} ads to match human copywriting, new emoticons, and multi-line signature.")

if __name__ == "__main__":
    main()

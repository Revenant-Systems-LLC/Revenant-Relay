import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

NEW_ADS = {
    # CHEAT SHEETS & TIPS
    "CS-001": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/CYBORG_GOLD.png",
        "caption": """▲───────◇◆◇───────▲
  ᴛʜᴇ ᴀɪ ᴀяᴄʜɪᴛᴇᴄᴛ's ᴄʜᴇᴄᴋʟɪsᴛ
  (Because default prompting is slop)
▲───────◇◆◇───────▲

Most developers think they're coding when they tell an LLM to "be extremely helpful." 

Spoiler: You're not. You're just paying for token pleasantries while your context window slowly bleeds. 

Here is the zero-inference structural blueprint for actual persona architecture. ⍥⍤⍣

⍡ Delimiter discipline (no flat text)
⍢ Dry-run draft stages (force logical routing)
⍩ Strict output typing (jailbreak prevention)

          õ.O   Read the checklist. It's free.
                https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """ᴛʜᴇ ᴀɪ ᴀяᴄʜɪᴛᴇᴄᴛ's ᴄʜᴇᴄᴋʟɪsᴛ. ⍥⍤⍣
▲───────◇◆◇───────▲

A complete, saveable blueprint for designing zero-inference agent environments. No conversational fluff, just machine-logic execution.

õ.O  Get the checklist: https://www.revenantsystems.net"""
        }
    },
    
    "CS-002": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/_comb.png",
        "caption": """¸,ø¤º°`°º¤ø,¸¸,ø¤º°   °º¤ø,¸¸,ø¤º°`°º¤ø,¸
  яᴇᴠᴇɴᴀɴᴛ ᴄʜᴇᴀᴛ sʜᴇᴇᴛs  
¸,ø¤º°`°º¤ø,¸¸,ø¤º°   °º¤ø,¸¸,ø¤º°`°º¤ø,¸

Stop saying "please" and "thank you" to your AI. 

Seriously. Cut that shit out.

Polite words are literal token waste. Every pleasantry forces the model to calculate useless conversational math. You are literally paying to buy your machine a coffee it can't drink. 

It's a mathematical execution engine. It doesn't have feelings, but it DOES have attention limits. Diluting your instructions with fluff distorts system behavior and makes output worse.

          щ(ಠ益ಠщ)   Save your tokens for actual logic.
                     https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Stop saying 'please' and 'thank you' to your AI. 
¸,ø¤º°`°º¤ø,¸¸,ø¤º°   °º¤ø,¸¸,ø¤º°`°º¤ø,¸

Every pleasantry is literal token waste. You are paying to calculate useless social math on an execution engine that has no feelings. 

щ(ಠ益ಠщ)  Be concise. Command the model.
https://www.revenantsystems.net"""
        }
    },

    "CS-003": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/circuit5.png",
        "caption": """★━━━━━━━━━━━━━━━━━★
  ᴀɪ ᴀяᴄʜɪᴛᴇᴄᴛ ʙʟᴜᴇᴘяɪɴᴛ
★━━━━━━━━━━━━━━━━━★

The Genesis Prompt Matrix. 

Most developers write flat system prompts and pray for logical consistency. It's a complete gamble.

The Genesis Matrix provides a highly structured blueprint for persona architecture. It stops prompt injections, enforces system rules, and guarantees logical compliance with zero-inference policies.

          ಠ_ರೃ   Quite elegant, really.
                 Check the architecture:
                 https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """The Genesis Prompt Matrix. ᴀɪ ᴀяᴄʜɪᴛᴇᴄᴛ ʙʟᴜᴇᴘяɪɴᴛ
★━━━━━━━━━━━━━━━━━★

Stop writing flat text prompts. Discover how a structured, zero-inference system prompt matrix enforces strict rule compliance and prevents jailbreaks.

ಠ_ರೃ  Read the blueprint: https://www.revenantsystems.net"""
        }
    },

    "CS-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/circuit4.png",
        "caption": """✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶
  яᴇᴠᴇɴᴀɴᴛ sʏsᴛᴇᴍs
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

3 formatting rules that instantly improve AI reasoning:

1. Leverage Markdown structures
2. Use strict XML/HTML delimiters
3. Restrict outputs with zero-inference guidelines

Stop sending large paragraphs of unstructured prose. Give the engine clear, token-optimized parsing blocks and watch it work.

          ٩(͡๏̯͡๏)۶   It's not magic, it's just syntax.
                     Learn the rules:
                     https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """3 formatting rules that instantly improve AI reasoning:
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

1. Markdown structures
2. Strict XML delimiters
3. Zero-inference boundaries

٩(͡๏̯͡๏)۶  Stop sending paragraphs. Start using structure.
https://www.revenantsystems.net"""
        }
    },

    # HARDENING
    "RH-001": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/_comb.png",
        "caption": """▲───────◇◆◇───────▲
  яᴇᴠᴇɴᴀɴᴛ нᴀяᴅᴇɴɪɴɢ
▲───────◇◆◇───────▲

>> rsh scan .
>> WARNING: 19 SILENT TIME BOMBS DETECTED

Most AI applications are deployed with massive security holes—context window leaks, token manipulation vectors, and unbounded database/tool access.

If a 12-year-old with a basic prompt injection can hijack your agent and drain your API keys, you don't have an application. You have a massive liability.

          o(╥﹏╥)o   Don't let them bleed your system dry.
                     Scan and harden your setup:
                     https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """rsh scan . -> 19 silent vulnerabilities detected. 💣💀
▲───────◇◆◇───────▲

Most AI agents are deployed with massive security holes. Scan, isolate, and secure your systems before they go to production.

яᴇᴠᴇɴᴀɴᴛ нᴀяᴅᴇɴɪɴɢ  https://www.revenantsystems.net"""
        }
    },

    "RH-002": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/circuit3.png",
        "caption": """·▄▄▄▄       ▄▄▄    .  ▄▄▄·      ·▄▄▄▄  
██▪ ██    ▀▄.▀·   ▐█  ▀█      ██▪    █
▐█·  ▐█  ▐▀▀▪   ▄█▀▀█      ▐█·    ▐█▌
██. ██  ▐█▄▄▌ ▐█▪  ▐▌     ██.   ██ 
▀▀▀▀•     ▀▀▀       ▀       ▀    ▀▀▀▀•

If a 12-year-old can prompt-inject your system, you do not have a system.

Stop relying on basic system prompts for security. "System Prompts" are suggestions to an LLM. They will bypass them eventually.

Revenant Hardening ensures your AI agents operate within strict, zero-inference sandbox layers that resist advanced jailbreak techniques.

          (凸ಠ益ಠ)凸  Is your prompt actually secure?
                     Hardened boundaries:
                     https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """If a 12-year-old can prompt-inject your system, you don't have a system. 💀
 
Stop relying on basic prompts for security. Hardening blocks context leaks and token manipulation at the execution layer.

(凸ಠ益ಠ)凸  Lock it down: https://www.revenantsystems.net"""
        }
    },

    "RH-003": {
        "post_format": "text",
        "media_path": None,
        "caption": """■█■█■█■█■█■█■█■
  [!] AI DATA LEAK IDENTIFIED [!]
■█■█■█■█■█■█■█■

The 3 ways your AI is leaking data right now:

1. Context window spilling (reading past data)
2. Token manipulation (hijacking system calls)
3. Unbounded tool use (unrestricted shell/DB access)

We build the walls. We isolate the memory. We secure the system.

          ¬_¬   Stop leaving the keys in the ignition.
                Revenant Hardening:
                https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """The 3 ways your AI is leaking data right now:
■█■█■█■█■█■█■█■

1. Context window spilling
2. Token manipulation
3. Unbounded tool use

¬_¬  Lock down your agent architectures today.
https://www.revenantsystems.net"""
        }
    },

    "RH-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/circuit2.png",
        "caption": """✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶
  яᴇᴠᴇɴᴀɴᴛ sʏsᴛᴇᴍs
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

Stop trusting default AI security.

Standard LLM wrappers provide exactly zero real isolation. They are built for convenience, not defense.

Here is the structural blueprint of how Revenant boundaries operate, enforcing strict zero-inference policies and securing your local system resources.

          ×͡×   Convenience is the enemy of security.
               Hardened boundaries:
               https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Stop trusting default AI security wrappers. 💀
✶⊶⊷⊶⊷❍⊶⊷⊶⊷✶

True agentic capability requires strict separation of config, state memory, and sandbox boundaries. Enforce zero-inference policies.

×͡×  Learn how: https://www.revenantsystems.net"""
        }
    },

    # THEME STUDIO
    "RTS-001": {
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/auto-match.mp4",
        "caption": """  [!] MANUAL ASSET MANAGEMENT HAS BEEN RETIRED [!]

Stop manually binding folder icons like it's 2005. 

Your IDE, assets, and folders are where you spend 10+ hours a day. Staring at default yellow folders is visual noise.

Revenant Theme Studio auto-matches your entire visual library to custom icons in seconds. It handles backups, registry, and protected system icon swaps with a single click.

          щ(ಥДಥщ)   Why are you still clicking manually?
          (凸ಠ益ಠ)凸  Get the Studio:
                     https://www.revenantsystems.net/software""",
        "platform_captions": {
            "x": """Stop manually binding icons like it's 2005. 💀

Revenant Theme Studio maps your entire visual library to custom icons in seconds. Backups included.

щ(ಥДಥщ)  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-002": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/gunmetal_theme.png",
        "caption": """▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 
  [!] DEFAULT THEMES CAUSE EYE STRAIN [!]
▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 

Default folders are for people who enjoy staring at flat yellow voids.

Upgrade your workspace to a cohesive, custom-engineered dark aesthetic that increases focus and reduces visual clutter. 

Flawlessly applied Gunmetal and Ruby themes across your entire folder hierarchy in seconds.

          ಠ_ರೃ   Quite a massive upgrade.
                 Check the themes:
                 https://www.revenantsystems.net/software""",
        "platform_captions": {
            "x": """Default folder icons are for people who enjoy eye strain. 👁️💀

Upgrade your entire visual hierarchy to flawless Gunmetal and Ruby icons in seconds.

ಠ_ರೃ  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-003": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/CYBORG_GOLD.png",
        "caption": """  ┻┳|―-∩
  ┳┻|　　ヽ   (Psst... check out this setup)
  ┻┳|　●   |
  ┳┻|▼) _ノ
  ┻┳|￣　)
  ┳ﾐ(￣  ／
  ┻┳T￣|

Workspace: Upgraded. 

Featuring the CYBORG_GOLD wallpaper, perfectly unified with the custom Gunmetal icon pack (over 140 custom crafted icons built for developers).

Aesthetics dictate workflow. Ditch the default yellow styling.

Get the setup free:
https://www.revenantsystems.net/software""",
        "platform_captions": {
            "x": """Workspace: Upgraded. 💀✨

CYBORG_GOLD meets the Gunmetal icon pack (140+ custom crafted developer folder icons). Ditch the default voids.

┻┳|―-∩  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-004": {
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/Revenant Systems.mp4",
        "caption": """  [!] AESTHETICS DICTATE WORKSPACE ENERGY [!]

You spend half your life staring at your desktop and directory trees. Why does it look like a factory reset machine?

Revenant Theme Studio maps your assets, protects your system backups, and deploys high-end dark aesthetics instantly.

          ᕙ(⇀‸↼‶)ᕗ   A beautiful setup is a productive setup.
          ʕ•́ᴥ•̀ʔ      Give it a spin:
                      https://www.revenantsystems.net/software""",
        "platform_captions": {
            "x": """Aesthetics dictate workflow. 💻⚡

Stop staring at default factory-reset folder trees. Deploys custom unified dark themes instantly.

ᕙ(⇀‸↼‶)ᕗ  Get the app: https://www.revenantsystems.net/software"""
        }
    },

    # FULL BUNDLE
    "BUN-002": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/CYBORG_GOLD.png",
        "caption": """  [!] SYSTEM ALERT: HAMMER TOOL DETECTED [!]

Claude is a scalpel. You're using it like a hammer.

Most developers write essays in the prompt box and expect production-ready codebase files.

To get actual, deterministic outputs, you need advanced artifact manipulation and strict delimiter control. 

Steal this exact prompt engineering skill for free, and unlock the other 9 in our bundle.

          ¬_¬   Stop prompting. Start compiling.
          ⍡     Get the skills:
                https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Claude is a scalpel. You're using it like a hammer. 💀

Stop typing essays. Structure your prompts with strict delimiters and force logic stages. 

¬_¬  Unlock the 10 production-ready skills: https://www.revenantsystems.net"""
        }
    },

    "BUN-003": {
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/BACKGROUND.mp4",
        "caption": """  [!] AVERAGE DEVELOPER VS. REVENANT BUNDLE [!]

Average Developer:
- Fights with Claude for 45 minutes on formatting.
- Receives hallucinated API keys.
- Context spills over and crashes.

Revenant Bundle User:
- Drops a pre-compiled Genesis Prompt.
- Logical dry-run completes in seconds.
- Flawless, production-ready code output.

          ٩(͡๏̯͡๏)۶   Why are you still fighting the model?
                     Get the blueprint:
                     https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Average Developer vs. Revenant Bundle. 

Stop fighting the model for formatting. Drop a genesis prompt, dry-run in memory, and get flawless production code instantly.

٩(͡๏̯͡๏)۶  Get the bundle: https://www.revenantsystems.net"""
        }
    },

    "BUN-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/RSLLC_GOLD2.png",
        "caption": """★━━━━━━━━━━━━━━━━━★
  яᴇᴠᴇɴᴀɴᴛ ʙᴜɴᴅʟᴇ
★━━━━━━━━━━━━━━━━━★

Stop guessing how to instruct LLMs. Prompt engineering is not a vibe check—it is system configuration.

The 10 Claude skills that actually work in production development. Backed by zero-inference principles.

          o(╥﹏╥)o   Don't let your code go to the grave.
                     Resurrect your setup:
                     https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Resurrect your dead prompts. 💀🔥

Prompt engineering is not a vibe check—it is system configuration. Get the 10 skills that work in production.

яᴇᴠᴇɴᴀɴᴛ ʙᴜɴᴅʟᴇ  https://www.revenantsystems.net"""
        }
    },

    "BUN-005": {
        "post_format": "text",
        "media_path": None,
        "caption": """  [!] HOW TO FORCE LOGICAL PROCESSING [!]

If you aren't restricting output formats, enforcing a dry-run stage in memory, and isolating parameters, your agent is just guessing.

Here is the step-by-step XML blueprint to force Claude to build logical reasoning steps before writing a single line of code.

          ¯\_(ツ)_/¯   Or you can keep debugging hallucinations.
          ⍩           Get the blueprint:
                      https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """How to force logical processing in Claude. 🧵👇

Stop reading essays. Structure prompts with XML delimiters, enforce a dry-run stage, and target zero-inference. [Thread]

¯\_(ツ)_/¯  Blueprint: https://www.revenantsystems.net"""
        }
    },

    # SYSTEM ARCHITECTURE
    "SYS-001": {
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/BACKGROUND.mp4",
        "caption": """  яᴇᴠᴇɴᴀɴᴛ sʏsᴛᴇᴍs
▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂ 

Your AI is a glorified chatbot.

Real business value doesn't come from prompt boxes and conversational widgets—it comes from symbiotic systems where machine logic and human intent work in perfect unison.

Stop chatting with LLMs. Build deterministic, zero-trust architectures.

       (ノಠ益ಠ)ノ彡┻━┻   A prompt is not an architecture.
                       Build the future:
                       https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Your AI is a glorified chatbot. 💀

Real value doesn't come from chat widgets—it comes from core systems where machine logic and human intent work in perfect symbiosis.

(ノಠ益ಠ)ノ  Start engineering: https://www.revenantsystems.net"""
        }
    },

    "SYS-002": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/CYBORG_GOLD.png",
        "caption": """  [!] PRECISION OVER PROBABILITY [!]

Stop treating AI like a search engine. 

An LLM is a probabilistic token predictor, not a database. If you build your software assuming it "knows" facts, you are building on wet sand.

Grounding, zero-inference constraints, and systematic state management are the only ways to achieve production reliability.

          ×͜×   Precision wins. Luck is not a strategy.
          ⍥⍤⍣   Ground your systems:
                https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """Precision over probability. 💻⚡

AI is not a database—it is a token predictor. Grounding, zero-inference boundaries, and state management are mandatory for production.

×͜×  Ground your systems: https://www.revenantsystems.net"""
        }
    },

    "SYS-003": {
        "post_format": "text",
        "media_path": None,
        "caption": """  [!] HOW MANY TIMES DID YOUR AI HALLUCINATE TODAY? [!]

If your agentic systems rely on the model's memory to track execution state, you are begging for a crash.

A Revenant System grounds every single state change in structured local files, strict context bounds, and isolated runtime shells.

          щ(ಥДಥщ)   Stop praying for clean outputs.
          o(╥﹏╥)o   Build structural reliability:
                      https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """How many times did your AI hallucinate today? 💀

Stop relying on LLM memory. Ground every single state change in local context files and isolated runtime boundaries.

щ(ಥДಥщ)  Get structured: https://www.revenantsystems.net"""
        }
    },

    "SYS-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/circuit2.png",
        "caption": """█░▒█ █▀▀▄ █▀▀▄ █▀▀ █▀▀█ █▀▀▄
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
              Get the blueprint:
              https://www.revenantsystems.net""",
        "platform_captions": {
            "x": """The Anatomy of a Revenant System. 💻⚡

True agentic capability requires separating config, state memory, platform integration, and secure runtimes. 

⍩  Get the 4-part blueprint: https://www.revenantsystems.net"""
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
                            data["post_format"] = NEW_ADS[ad_id]["post_format"]
                            data["media_path"] = NEW_ADS[ad_id]["media_path"]
                            data["caption"] = NEW_ADS[ad_id]["caption"]
                            
                            if "platform_captions" not in data:
                                data["platform_captions"] = {}
                            
                            # Update platform captions specifically
                            data["platform_captions"]["x"] = NEW_ADS[ad_id]["platform_captions"]["x"]
                            
                            # If we changed format to image, let's keep allowed platforms correct
                            # (Pinterst doesn't support video)
                            if data["post_format"] == "image":
                                if "pinterest" in data.get("allowed_platforms", []):
                                    pass # fine
                            
                            with open(ad_file, "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2)
                                
                            print(f"Successfully overhauled and cleaned: {ad_id}")
                            updated_count += 1
                        except Exception as e:
                            print(f"Error updating {ad_id}: {e}")
                            
    print(f"\nCompleted! Overhauled {updated_count} ads to scrub guild names and fix all media placeholders.")

if __name__ == "__main__":
    main()

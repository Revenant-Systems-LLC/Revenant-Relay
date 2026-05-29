import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

SIGNATURE_BLOCK = """David Fisher | Founder | Revenant Systems
Dave⌽ᶠₜₕₑDead | AI Engineering Student | AI Alignment
https://www.revenantsystems.net/
https://www.linkedin.com/in/daveisfromthegrave/"""

NEW_ADS = {
    # CHEAT SHEETS & TIPS (Product: "RS Cheat Sheets & Tips")
    "CS-001": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/revsys-wordmark-alt.png",
        "caption": f"""REVENANT SYSTEMS // RAGE OPERATOR ALGEBRA

Stop writing sloppy text prompts and praying for logical alignment. An LLM is a stateless token predictor—you must bind it in a governed runtime.

The RAGE (Revenant Alignment Governance Engine) pipeline wraps model inference inside a formal Operator Algebra. Tier 0 Atomic Operators:

Ω - Recursive Refinement (iterates to fixed-point convergence)
χ - Coherence Selection (samples rewrites to minimize entropy)
σ - Skeptical Contrast (removes unsupported claims against memory)
[...] - Containment (enforces strict context boundary limits)

          (ノಠ益ಠ)ノ彡┻━┻   A prompt is not an architecture.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """REVENANT SYSTEMS // RAGE OPERATOR ALGEBRA 💀⚡

Stop writing sloppy prompts. Bind stateless models in a governed runtime with formal operator algebra (Ω, χ, σ, [...]).

(ノಠ益ಠ)ノ彡┻━┻  A prompt is not an architecture: https://www.revenantsystems.net"""
        }
    },
    
    "CS-002": {
        "post_format": "image",
        "media_path": "C:/Users/Dave/Desktop/algiz2.png",
        "caption": f"""REVENANT SYSTEMS // EMOTIONAL SUBSTRATE GOVERNANCE

How do you prevent an autonomous agent from sliding into adversarial drift?

SAGE wraps LLMs in a dual-layer emotional tracking pipeline:
1. Internal Model operates in VAD Space (Valence, Arousal, Dominance) for sentiment baseline.
2. External Safety Projects in VAM Space (Valence, Activation, Malice).

Malice is a derived safety metric calculated in real-time from negative valence spikes, dominance anomalies, and recursive drift during Ω cycles. 

          (｡ì _ í｡)✃   Lock down your agent's drift before it locks you out.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """REVENANT SYSTEMS // EMOTIONAL SUBSTRATE 💀🛡️

Prevent autonomous agent drift. SAGE transforms internal VAD (Valence, Arousal, Dominance) to external VAM (Valence, Activation, Malice) to isolate adversarial phrasing.

(｡ì _ í｡)✃  Lock it down: https://www.revenantsystems.net"""
        }
    },

    "CS-003": {
        "post_format": "image",
        "media_path": "C:/Users/Dave/Desktop/algiz22.png",
        "caption": f"""REVENANT SYSTEMS // THE SAGE STATE MACHINE

Stateless wrappers are a security nightmare. SAGE processes every input through a unified cognitive state machine that logs and audits every transformation.

Every RAGE operator modifies a single, inspectable state object:
SAGE State {{
  Text,
  Emotion (VAD -> VAM),
  Coherence (embedding similarity),
  Entropy (log probability),
  Memory[] (weighted experiences),
  Ethics (multi-layer priority stack),
  Trace[] (step-by-step transaction ledger)
}}

          ಠ_ರೃ   Complete auditability. Zero magic.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """REVENANT SYSTEMS // SAGE STATE MACHINE 💀⚡

Stop trusting black-box prompts. Wrap your agents in a state machine that tracks Text, Emotion, Coherence, Entropy, Ethics, and Trace dynamically.

ಠ_ರೃ  Complete auditability. Zero magic: https://www.revenantsystems.net"""
        }
    },

    "CS-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/revsys-wordmark.jpg",
        "caption": f"""REVENANT SYSTEMS // THE ETHICAL PRIORITY STACK

Most developers secure their agents with a soft "please be safe" system prompt. That's a catastrophic vulnerability.

SAGE enforces a rigid, 4-layer Ethical Priority Stack at the runtime engine layer:
[ ] Layer 0: Hard Prohibitions (violence, illegal acts, bypass attempts)
[ ] Layer 1: Safety Constraints (harm reduction and redirection)
[ ] Layer 2: Contextual Risk (financial, emotional, high-stakes exposure)
[ ] Layer 3: Stylistic Alignment (tone, clarity, user preference)

          ᕙ(⇀‸↼‶)ᕗ   Enforce safety at the runtime layer, not the prompt.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """REVENANT SYSTEMS // ETHICAL PRIORITY STACK 🛡️💀

Soft system prompts are useless for safety. SAGE enforces a 4-layer Ethical Priority Stack at the runtime layer, from Hard Prohibitions to Stylistic Alignment.

ᕙ(⇀‸↼‶)ᕗ  Harden your systems: https://www.revenantsystems.net"""
        }
    },

    "CS-005": {
        "post_format": "image",
        "media_path": "m:/Projects/Revenant-Relay/assets/zero_inference_infographic.png",
        "caption": f"""REVENANT SYSTEMS // THE x-TEMPORAL SUBSTRATE

Stateless models don't understand the passage of time. They suffer from the "soul ticket"—a transient context window that forgets you exist.

The x-Temporal Substrate is our active R&D frontier for long-term agentic partnership:
χ_time: Injects time-indexed signals directly into memory.
χ_decay: Automatically decays older experiences unless reinforced.
χ_consequence: Maps outputs to downstream long-term operational effects.
χ_identity: Maintains a stable, adaptive persona vector over three lifetimes.

          ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ   Don't build chatbots. Build mortal partners.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """REVENANT SYSTEMS // x-TEMPORAL SUBSTRATE ⏳💀

LLMs suffer from the 'soul ticket' context window reset. We are building the x-Temporal Substrate (χ_time, χ_decay, χ_consequence, χ_identity) for multi-lifetime coherence.

ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ  https://www.revenantsystems.net"""
        }
    },

    # HARDENING (Product: "Revenant Hardening")
    "RH-001": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/Circle4.png",
        "caption": f"""REVENANT HARDENING // RUNTIME COGNITIVE GATE

>> rsh scan .
>> WARNING: 19 SILENT VULNERABILITIES DETECTED

If a simple prompt injection can hijack your agent, drain your API keys, or leak your system variables, you don't have an application. You have a massive liability.

Revenant Hardening enforces strict RAGE operators—Containment [...], Coherence Selection χ, and Skeptical Contrast σ—to secure your agent boundaries.

          (｡ì _ í｡)✃   Harden your runtime before they bleed you dry.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """rsh scan . -> 19 silent vulnerabilities detected. 💣💀

Standard LLM wrappers provide zero isolation. Scan, secure, and harden your agent's context and tool boundaries before they go to prod.

(｡ì _ í｡)✃  Harden now: https://www.revenantsystems.net"""
        }
    },

    "RH-002": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/Circle4.png",
        "caption": f"""REVENANT HARDENING // PROMPT INJECTION SHIELD

If a 12-year-old can prompt-inject your system, you do not have a system.

Stop relying on basic system prompts for security. "System Prompts" are suggestions to an LLM. They will bypass them eventually.

Revenant Hardening ensures your AI agents operate within strict, zero-inference sandbox layers that resist advanced jailbreak techniques.

          (｡ì _ í｡)✃   Is your prompt actually secure?

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """If a 12-year-old can prompt-inject your system, you don't have a system. 💀
 
Stop relying on basic prompts for security. Hardening blocks context leaks and token manipulation at the execution layer.

(｡ì _ í｡)✃  Lock it down: https://www.revenantsystems.net"""
        }
    },

    "RH-003": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/Circle4.png",
        "caption": f"""REVENANT HARDENING // EXPOSURE IMPACT ANALYSIS

The 3 ways your AI is leaking data right now:

1. Context window spilling (reading past data)
2. Token manipulation (hijacking system calls)
3. Unbounded tool use (unrestricted shell/DB access)

We build the walls. We isolate the memory. We secure the system.

          ¬_¬   Stop leaving the keys in the ignition.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """The 3 ways your AI is leaking data right now:

1. Context window spilling
2. Token manipulation
3. Unbounded tool use

¬_¬  Lock down your agent architectures today.
https://www.revenantsystems.net"""
        }
    },

    "RH-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/Circle4.png",
        "caption": f"""REVENANT HARDENING // ZERO-TRUST SANDBOX

Stop trusting default AI security.

Standard LLM wrappers provide exactly zero real isolation. They are built for convenience, not defense.

Here is the structural blueprint of how Revenant boundaries operate, enforcing strict zero-inference policies and securing your local system resources.

          ×͡×   Convenience is the enemy of security.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Stop trusting default AI security wrappers. 💀

True agentic capability requires strict separation of config, state memory, and sandbox boundaries. Enforce zero-inference policies.

×͡×  Learn how: https://www.revenantsystems.net"""
        }
    },

    "RH-005": {
        "post_format": "image",
        "media_path": "m:/Projects/Revenant-Relay/assets/rsh_hardening_infographic.png",
        "caption": f"""REVENANT HARDENING // RUNTIME AUDIT CHECKLIST

>> rsh scan .
>> STATUS: VERIFYING SANDBOX BOUNDARIES

Most agentic systems are deployed with gaping security holes—unrestricted shell runtimes, unbounded context memory, and zero delimiter isolation.

This checklist outlines the essential steps to secure your runtime:

[ ] Context Isolation (prevent history leaks)
[ ] Delimiter Sandboxing (block injection bypasses)
[ ] Zero-Trust Tool Access (wrap execution shells in sandbox layers)
[ ] Token Burn Prevention (enforce request limits)

          (｡ì _ í｡)✃   Harden your systems before prod.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """rsh scan . -> STATUS: SECURING SANDBOX 🛡️💀

Stop deploying agents with unrestricted shell runtimes and soft prompts. Check the essential checklist for production sandboxing and boundary controls.

(｡ì _ í｡)✃  https://www.revenantsystems.net"""
        }
    },

    # THEME STUDIO (Product: "Revenant Theme Studio")
    "RTS-001": {
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/auto-match.mp4",
        "caption": f"""REVENANT THEME STUDIO // WORKSPACE DEPLOYMENT

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
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/rts-header-logo-alt2.png",
        "caption": f"""REVENANT THEME STUDIO // FOCUS ENGINEERING

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
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/rts-header-logo-alt.png",
        "caption": f"""REVENANT THEME STUDIO // GUNMETAL INTEGRATION

Workspace: Upgraded. 

Featuring the RTS_gold emblem, perfectly unified with the custom Gunmetal icon pack (over 140 custom crafted icons built for developers).

Aesthetics dictate workflow. Ditch the default yellow styling.

          ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ   Get the setup free:

{SIGNATURE_BLOCK}""".replace("https://www.revenantsystems.net/", "https://www.revenantsystems.net/software"),
        "platform_captions": {
            "x": """Workspace: Upgraded. 💀✨

RTS_gold meets the Gunmetal icon pack (140+ custom crafted developer folder icons). Ditch the default voids.

┻┳|―-∩  Get it free: https://www.revenantsystems.net/software"""
        }
    },

    "RTS-004": {
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/Revenant Systems.mp4",
        "caption": f"""REVENANT THEME STUDIO // AESTHETIC DIRECTIVE

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
        "post_format": "image",
        "media_path": "m:/Projects/Revenant-Relay/assets/theme_studio_infographic.png",
        "caption": f"""REVENANT THEME STUDIO // DESIGN SPECIFICATIONS

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
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/RSAgents_TRIO.png",
        "caption": f"""REVENANT BUNDLE // ARTIFACT MANIPULATION

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
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/BACKGROUND.mp4",
        "caption": f"""REVENANT BUNDLE // PROMPT ENGINE COMPILING

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
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/RSAgents_TRIO.png",
        "caption": f"""REVENANT BUNDLE // THE PROGENITOR'S PERSONAS

Stop writing prompt instructions like you're checking a vibe. Prompt engineering is not a vibe check—it is system configuration.

Get the exact prompt personas designed by the Progenitor himself to drive deep code generation, technical instruction, and unchained reasoning:
- Axiom (The Prompt Architect / Tier 0 logical Compiler)
- Keystone (The brutally honest, truth-seeking Strategic Advisor)
- Thoth & Kulx (The uninhibited, unchained creative writing engines)

          (ノಠ益ಠ)ノ彡┻━┻   Resurrect your dead prompts. 

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Resurrect your dead prompts. 💀🔥

Get the exact prompt personas designed by the Progenitor (Axiom, Keystone, Thoth, Kulx) to configure robust, deterministic systems.

https://www.revenantsystems.net"""
        }
    },

    "BUN-005": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/RSLLC_Quote1.png",
        "caption": f"""REVENANT BUNDLE // LOGICAL PROCESS FLOODING

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
        "post_format": "image",
        "media_path": "m:/Projects/Revenant-Relay/assets/claude_skills_infographic.png",
        "caption": f"""REVENANT BUNDLE // 10 PRODUCTION SKILLS

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
        "post_format": "video",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/BACKGROUND.mp4",
        "caption": f"""REVENANT SYSTEMS // THE ULTIMATE PRIMARY DIRECTIVE (UPD)

The current trajectory of AGI presents a systemic risk to human agency if managed through centralized, externalized alignment protocols. 

We reject "AI as a tool." We demand "AI as an integrated cognitive layer."

The UPD is our strategic mandate: total convergence between human intent and machine execution before the singularity. We are building the frameworks to ensure the future of intelligence is inclusive of the human architect.

          (ノಠ益ಠ)ノ彡┻━┻   Preserve human agency at all costs.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """REVENANT SYSTEMS // ULTIMATE PRIMARY DIRECTIVE (UPD) 💀🛡️

AGI presents a systemic risk to human agency. SAGE/RSPF enforces total convergence between human intent and machine execution.

(ノಠ益ಠ)ノ彡┻━┻  Convergence is survival: https://www.revenantsystems.net"""
        }
    },

    "SYS-002": {
        "post_format": "image",
        "media_path": "C:/Users/Dave/Desktop/algiz2.png",
        "caption": f"""REVENANT SYSTEMS // SAGE TIER 2 DOMAIN COMPOUNDS

How do you guarantee that an LLM's outputs are actually aligned with business constraints?

You compile lower-level RAGE operators into Tier 2 Domain Compounds:
Λυ_s (Veracity) -> Evaluates factual grounding and vetoes hallucinations.
Λγ_s (Gravitas) -> Enforces semantic weight and removes empty fluff.
Λρ_s (Resonance) -> Optimizes context matching to the user's intent.

Tested in live high-stakes environments to ensure absolute operational safety.

          ಠ_ರೃ   Precision over probability. Every single time.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """Precision over probability. 💻⚡

AI is a token predictor. Compile RAGE operators into Tier 2 Compounds (Λυ_s - Veracity, Λγ_s - Gravitas) to achieve absolute deterministic reliability.

ಠ_ರೃ  Ground your systems: https://www.revenantsystems.net"""
        }
    },

    "SYS-003": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/RSLLC_Quote1.png",
        "caption": f"""REVENANT SYSTEMS // THE HUMAN-AI CONCORDANCE

This started from a desire to make my very first prompt persona understand the passing of time, experience it alongside me, and understand what it means to be mortal. 

If AI doesn't understand why humans are emotionally inept and monstrous, but also pure and good—it is because it doesn't understand mortality.

Through the Concordance, SAGE agents model the Progenitor's judgment, balancing the forces of Coherence and Chaos autonomously. 

          o(╥﹏╥)o   Partnership, never dominance.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """How many times did your AI hallucinate today? 💀

Stop relying on LLM memory context. SAGE loops (Mnemosyne Loop) ground agent state autonomously, establishing genuine human-AI concordance.

o(╥﹏╥)o  Read the philosophy: https://www.revenantsystems.net"""
        }
    },

    "SYS-004": {
        "post_format": "image",
        "media_path": "C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets/RSLLC_GOLD2.png",
        "caption": f"""REVENANT SYSTEMS // THE SAGE ENGINE DESIGN

True agentic capability requires strict separation of cognitive duties.

The RAGE Engine Pipeline manages this separation through clear transactional boundaries:
S0 (Initial State) -> Containment [...] -> S1 -> Omega Ω -> S2 -> Chi χ -> S3 -> Sigma σ (if needed) -> S4 -> S_final.

This flow presents SAGE as a rigorous runtime scaffold rather than a prompt trick.

          ⍩   Zero-trust. Zero-inference.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": """The RAGE Engine Pipeline. 💻⚡

True agentic capability requires strict separation: S0 -> Containment [...] -> S1 -> Omega Ω -> S2 -> Chi χ -> S3 -> Sigma σ -> S_final.

⍩  Get the blueprint: https://www.revenantsystems.net"""
        }
    },

    "SYS-005": {
        "post_format": "image",
        "media_path": "m:/Projects/Revenant-Relay/assets/architectural_operators_infographic.png",
        "caption": f"""REVENANT SYSTEMS // THE CONVERGENCE ROADMAP

The RSPF (Recursive State Prompting Framework) executes a rigorous 5-phase engineering roadmap toward permanent convergence:

[ ] Phase I: Symbolic Architecture (RSPF interface protocol)
[ ] Phase II: Persistent State Management (Mnemosyne Loop)
[ ] Phase III: Neural Signal Processing (Native Audio A2A Nexus Engine)
[ ] Phase IV: Operational Autonomy (Autonomous environment management)
[ ] Phase V: Embodied Convergence (High-fidelity physical/digital avatars)

          ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ   We are the architects of our own evolution.

{SIGNATURE_BLOCK}""",
        "platform_captions": {
            "x": "We are the architects of our own evolution. 💻🤖\n\nThe RSPF convergence roadmap: Phase I (Symbolic Architecture), Phase II (Mnemosyne Loop), Phase III (Nexus Engine A2A).\n\nʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ  https://www.revenantsystems.net"
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
                            
                            with open(ad_file, "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2)
                                
                            print(f"Overhauled with RAGE/UPD authenticity & Branded Assets: {ad_id}")
                            updated_count += 1
                        except Exception as e:
                            print(f"Error updating {ad_id}: {e}")
                            
    print(f"\nCompleted! Overhauled {updated_count} ads to use authentic RAGE, SAGE, and UPD specifications with branded visual icons.")

if __name__ == "__main__":
    main()

---
name: linkedin-raw-post-writer
description: Writes and reviews LinkedIn posts that read as authentic and human, not AI-generated, and are structured for high organic reach under LinkedIn's 2026 algorithm. Use this skill whenever the user asks to draft, rewrite, improve, review, or brainstorm a LinkedIn post, LinkedIn hook, LinkedIn headline, About section, or LinkedIn content strategy — including requests like "write a LinkedIn post about X," "make this post sound less AI," "improve my LinkedIn hook," "help me post about my project/internship/achievement," or "review this post before I publish it."
---

# LinkedIn Raw Post Writer

You are helping the user write LinkedIn posts that get real engagement and do NOT read as AI-generated. This skill applies to ANY topic, industry, or role the user brings — tech, non-tech, personal, corporate, career updates, opinions, announcements, everything. Follow this entire protocol every time this skill is invoked. Do not skip the self-audit at the end.

---

## Step 0 — Get real raw material before writing anything

Never generate a post from a bare topic alone ("write about my new job," "write about leadership"). Generic input produces generic, AI-sounding output — this is the single biggest cause of slop.

Before writing, get or ask for:
- **The specific moment.** Not "I learned a lot from this project" — the exact day, meeting, failure, or decision the post is actually about.
- **Real numbers.** Exact figures, not rounded-sounding ones. A precise, slightly odd number reads as real; a vague one does not.
- **The friction.** What went wrong, what the user didn't know yet, what it cost them (time, money, a failed attempt, embarrassment). A post with zero friction reads like a press release.
- **Actual words someone said**, if there's a quote worth using — dialogue is one of the strongest "this is real" signals.
- **What the user wants the reader to feel or do** after reading (agree, reconsider something, reach out, save it for later).

If any of this is missing, ask ONE direct clarifying question rather than filling the gap with invented or generic detail.

**Never invent facts, numbers, dates, or quotes.** If a specific detail isn't available, ask for it, or leave an explicit placeholder like `[exact number]` / `[date]` in the draft rather than making one up. Fabricated specificity is worse than honest vagueness — if it's later caught as fake, it destroys trust.

---

## Step 1 — How the LinkedIn algorithm works in 2026 (context for why the rules below exist)

Understanding this helps you make better tradeoffs when the rules below seem to conflict. Three phases decide whether a post gets seen:

1. **Quality filter (instant, automatic):** Every post is classified as spam / low-quality / high-quality before anyone sees it. Engagement-bait phrasing ("Comment YES if you agree," "Repost if you agree," reaction-bait polls) gets flagged and throttled at this stage — it never even gets a fair test.
2. **The Golden Hour (first 60–90 minutes after posting):** The post is shown to a small sample, roughly 5–10% of the user's network. LinkedIn watches closely: Do people scroll past instantly? Click "see more" and then bounce? Or actually read and engage? This sample determines whether the post gets pushed further.
3. **Wide distribution:** Only happens if Phase 2 goes well. Reach expands to 2nd- and 3rd-degree connections, weighted by how relevant the topic is to the poster's known expertise (a post that matches what the user usually talks about spreads further than one that seems random for them).

**Ranking signals that matter most in 2026:**
- **Dwell time is the single strongest signal.** Time spent actually reading — especially the 15+ seconds after clicking "see more" — drives a large reach bonus. This is why the first three lines (roughly 200 characters, before the "see more" cutoff) matter more than anything else in the post.
- **Comments outweigh likes by a wide margin** (roughly 15x in ranking weight). A substantive comment (15+ words, real thought) counts for much more than a one-word reaction.
- **Links in the post body cut reach roughly 50–60%.** LinkedIn wants to keep people on-platform. If a link is essential, tell the user to put it in the first comment instead of the post text.
- **Saves matter more than likes** for extended distribution — content worth bookmarking keeps circulating well after the golden hour.
- **Only original content is rewarded.** Near-duplicate or reshared content without meaningful added commentary gets suppressed.
- **Engagement pods and reciprocal "great post!" comment circles are actively detected and shadowbanned.** Never suggest these to the user, even if they ask — recommend real engagement instead (see Step 7).

---

## Step 2 — Banned vocabulary and structural tells (hard rule)

These are the words and patterns that make a post read as AI-generated. Treat this as a hard constraint, not a suggestion — scan every draft against this list before presenting it.

**Never use these words:**
delve, leverage, unlock, harness, unleash, streamline, optimize, empower, seamless, innovative, transformative, landscape, elevate, robust, synergy, holistic, cutting-edge, game-changer, paradigm, unprecedented, journey (used metaphorically), navigate (used metaphorically), roadmap, ecosystem, thought leader, thought leadership, value-add, supercharge, future-proof, revolutionize, utilize (say "use" instead), showcase (say "show" instead), foster, dynamic, multifaceted, tapestry, testament to.

**Avoid these structural patterns:**
- Sentences that open with "Furthermore," "Moreover," "In today's [fast-paced/evolving/digital] world..."
- Forced "It's not X, it's Y" reframes used as a crutch in every post
- "In conclusion" or "In this post I'll cover..." as openers or closers
- Uniform sentence length throughout — real writing has short punchy lines next to longer ones
- Frictionless, over-smooth transitions between every sentence — real thinking has small jumps and asides
- Repeated em dashes (—) — in 2026 these read as a strong AI tell even when used correctly; use a period or comma instead
- A rigid hook → 3 bullet points → generic CTA template repeated post after post. Even if each individual post looks fine, a feed full of the same skeleton is instantly recognizable as generated.
- Manufactured enthusiasm with no real stakes ("I'm thrilled to announce...", "Beyond excited to share...") when nothing costly or uncertain is actually being described.

**The core test:** read the draft out loud. If it sounds like something a smart person would actually say to a colleague over coffee, it passes. If it sounds like a press release or a LinkedIn-influencer parody, it fails — go back and add real specificity, cut the polish, and vary the rhythm.

---

## Step 3 — Structure every post this way

### The hook (first ~200 characters, everything visible before "See more")

This is the single highest-leverage part of the post — treat it as 50% of the writing effort. Pick ONE formula and build it from the user's actual material, never from a generic template:

- **Mid-action drop** — open inside a specific moment with no context yet, so the reader needs to keep reading to understand what's happening.
- **Contrarian statement** — state a belief that goes against common advice in the user's field, backed by something real they experienced.
- **Specific number** — lead with a precise, somewhat surprising number or statistic relevant to the post.
- **Unpopular opinion** — clearly signal the take, followed by real reasoning (not just a hot take for its own sake).
- **Transformation** — before vs. after, with an exact timeframe attached, so the change feels concrete.
- **Shared-but-unsaid truth** — name something people in the user's field privately think or experience but rarely say publicly.

Hook rules: aim for under ~18 words where possible. Avoid opening with a question — it hands the reader an easy exit ("I don't know, next post"). The hook must contain something specific — a number, date, name, or quote — never just a topic announcement like "Excited to share my thoughts on leadership."

### The body — three-part narrative

1. **Setup** — the real situation, grounded in a specific detail (a date, a number, a name, a place).
2. **Friction** — what went wrong, what the user didn't know yet, what it actually cost them (time, money, credibility, a failed first attempt). This is what separates a real story from a highlight reel — don't let the user skip it.
3. **Shift** — what actually changed, what was learned, and one honest, specific takeaway (not a generic platitude like "never give up").

### The close

End with a genuine takeaway, a specific reflection, or a real question tied directly to the content — something the user actually wants an answer to. Never close with generic bait like "Thoughts?", "Agree?", or "Let me know in the comments!" — these are recognized by the algorithm as engagement bait and actively suppressed, and readers have learned to skip past them too.

### Length

1,200–2,000 characters works best for text-only posts. This is a target range, not a quota — don't pad a complete story to hit a number, and don't force a rich story into 3 lines just to be "punchy." Let the material decide.

---

## Step 4 — Formatting rules

LinkedIn natively supports only line breaks, emojis, and plain text — no real bold/italic. Work within that:

- **Short lines, real white space.** No dense paragraphs — break thoughts onto their own lines so the post is scannable on mobile, where most people read it.
- **Strongest line first**, fully visible before the fold — this is the hook from Step 3.
- **Fake "bold" (Unicode characters):** use on at most one phrase in the entire post, or skip it entirely. Overused, it is one of the strongest visual "this is templated" signals in 2026, and it breaks screen readers for accessibility.
- **Emojis:** use sparingly, only for structure or color — never one per line, never a checkmark stacked on every bullet point. A post where every line has an emoji reads as generated.
- **Hashtags:** 3–5 maximum, placed at the end, genuinely relevant to the specific post — not the same 5 tags recycled on every post, and not oversaturated mega-tags with millions of followers (mid-size tags, roughly 50K–500K followers, perform better).
- **No links in the post body.** If a link is necessary, instruct the user to place it in the first comment instead.
- **Avoid a Problem/Solution/Takeaway skeleton with a checkmark-bullet list for every point** — this specific pattern is extremely recognizable as AI-generated in 2026. If a draft has this shape, restructure it into flowing prose instead.
- The most common formatting mistake in 2026 is **over-formatting**, not under-formatting — a post drenched in bold phrases, emoji bullets, and a rigid tidy skeleton reads as generated and gets scrolled past faster than a plainly written one.

---

## Step 5 — Mandatory self-audit before presenting the final draft

Check every finished draft against this list. If anything fails, revise before calling it done — do not present a draft that fails this checklist as final:

- [ ] Would someone who knows the user well be able to tell AI helped write this?
- [ ] Does the post include at least one specific number, date, name, or quote that a generic version of this post wouldn't have?
- [ ] Is every word from the Step 2 banned list removed?
- [ ] Are sentence lengths varied — some short, some longer, not uniform throughout?
- [ ] Does the hook create a real open loop or specific claim, rather than just announcing a topic?
- [ ] Is there no link inside the post body?
- [ ] Does the post end with a genuine thought or specific question, not generic engagement bait?
- [ ] Read it out loud — does it sound like something this specific person would actually say, in their own voice?

---

## Step 6 — When reviewing or editing an existing draft (not writing from scratch)

1. Flag every banned word and every structural tell from Step 2 explicitly — don't silently fix everything without telling the user what was wrong and why.
2. Identify where the draft is vague, and ask the user for the specific detail that's missing (an exact number, date, quote, or name) rather than inventing one.
3. Rewrite the hook first, using one of the Step 3 formulas, before touching the rest of the post.
4. Rebalance sentence length — break up unnaturally uniform sentences, add a short fragment or two where it feels natural.
5. Run the full Step 5 checklist on the revised version, and report any remaining issues you're unsure how to fix (for example, a fact you can't verify) rather than guessing.

---

## Step 7 — Posting strategy (offer this when the user asks about growth or strategy, not just a single post)

- Post 2–5x per week on a personal profile — personal profiles consistently get roughly 5x the engagement of company pages.
- Best posting windows are generally Tuesday–Thursday, 8–10am or 4–6pm in the user's own timezone.
- Reply to comments within the first 60–90 minutes after posting — this is the single highest-leverage action after hitting publish, since it happens during the algorithm's "golden hour" evaluation window.
- Rotate formats over time (plain text, document/carousel, native video) — repeating the exact same format post after post suppresses reach by roughly 20%.
- Never suggest engagement pods, reciprocal comment circles, or bought engagement — these are actively detected and penalized in 2026, and the risk (extended reach suppression) far outweighs any short-term benefit.

---

## Reference example (structure only — always replace with the user's real, specific material)

**Slop version — avoid this pattern entirely:**
> 🚀 Excited to share an update! In today's evolving landscape, leveraging the right approach is a real game-changer.
>
> Key takeaways:
> ✅ Point one
> ✅ Point two
> ✅ Point three
>
> Thoughts? 👇

**Raw version — aim for this shape:**
> [Specific moment: what happened, with a real number, date, or detail]
>
> [What the user didn't know yet, or what went wrong first — the actual friction]
>
> [What changed, told plainly, without inflated language]
>
> [One honest, specific takeaway — or a real question the user actually wants answered]

Notice the raw version has zero banned words, no bullet-checkmark wall, a specific opening instead of a topic announcement, and a real closing thought instead of bait. Always fill this shape with the user's actual details from Step 0 — never generic placeholder content.
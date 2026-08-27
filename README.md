# Cissy & Bud — Travel Website V1

A responsive, zero-build prototype for David and Cassie's travel-blog website. This repository treats the Google Doc **Travel Website** as the version-one canonical requirements source.

## Public preview

Once GitHub Pages is enabled, the site is available at:

**https://davidnombo.github.io/cissy-and-bud-travel/**

## What this prototype covers

- A story-first homepage designed for readers coming from Facebook and Instagram
- Travel-log cards with category filtering and story-preview dialogs
- A route section reflecting the 2026–2027 travel arc in the canonical document
- About/backstory area ready for a Nombo interview
- Patreon and print-on-demand concepts, deliberately secondary to the story
- Newsletter/CRM signup interface (demo only until a provider is selected)
- Responsive navigation and mobile layout
- Accessible landmarks, labels, keyboard-friendly controls, and reduced-motion support

## Recommended V1 architecture

1. **Home** — introduction, latest entries, route, support, and signup
2. **Journal** — filterable chronological travel log
3. **Journal entry** — prose, photos, an embedded Reel/short video, route location, date
4. **Our route** — trip map and current/next stops
5. **Our story** — David and Cassie's backstory
6. **Support** — Patreon explanation and membership link
7. **Shop** — a small print-on-demand catalog hosted by the selected commerce provider

The prototype combines these into one page so layout, brand, and priorities can be approved before separate pages are built.

## Content workflow recommendation

David and Cassie should **not edit HTML**. For V1:

1. Send Nombo a short note, selected photos, and an exported Reel.
2. Nombo drafts the entry and returns it for review.
3. After approval, Nombo publishes the entry to GitHub.
4. Store video on YouTube (or another video host) and embed it so the site stays fast and inexpensive.

A visual CMS can be added later if direct self-service editing becomes more important than keeping the first launch simple.

## Decisions needed after prototype review

- Confirm or replace the working brand **Cissy & Bud** and tagline **The Long Way Home**.
- Choose 6–12 strong photos for the first public release.
- Complete a short About Us interview.
- Choose an email provider (MailerLite is a strong low-cost starting point).
- Decide whether Patreon and the store launch with the blog or in a second release.
- Select and purchase a domain; point it to GitHub Pages.

## Local preview

No build tools are required:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Current limitations

- Story content and portraits are labeled placeholders.
- Newsletter submission is an in-browser demo and does not store addresses.
- Social links, Patreon, and shop links remain inactive until final accounts are selected.
- The route illustration is intentionally conceptual rather than turn-by-turn navigation.

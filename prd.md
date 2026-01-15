# Product Requirements Document (PRD)
## Flux - Capture cognitive instantanée

**Version:** 1.0  
**Date:** 14 Janvier 2026  
**Auteur:** Tom  
**Statut:** Draft - Phase MVP

---

## Table des matières

1. [Vision & Problème](#1-vision--problème)
2. [Objectifs](#2-objectifs)
3. [Personas & Use Cases](#3-personas--use-cases)
4. [Scope MVP](#4-scope-mvp)
5. [User Flows](#5-user-flows)
6. [Spécifications Techniques](#6-spécifications-techniques)
7. [Design & UX](#7-design--ux)
8. [Success Metrics](#8-success-metrics)
9. [Out of Scope](#9-out-of-scope)
10. [Risks & Mitigations](#10-risks--mitigations)
11. [Timeline](#11-timeline)
12. [Open Questions](#12-open-questions)

---

## 1. Vision & Problème

### 1.1 Vision (One-liner)

> **"L'app de capture cognitive la plus rapide au monde pour les cerveaux qui pensent plus vite qu'ils n'écrivent"**

### 1.2 Problème Utilisateur

**Contexte ADHD / Troubles de l'attention:**
- 15-20 pensées par jour méritent d'être capturées (idées, tâches, insights)
- Le délai entre "idée" et "app ouverte" est trop long → **idée perdue**
- Les apps actuelles forcent des décisions (dossier? titre? format?) → **paralysie décisionnelle**
- Impossible de retrouver les notes capturées → **abandon progressif du système**
- Charge mentale constante: "J'oublie de ne pas oublier"

### 1.3 Solution Proposée

**Input instantané sans friction:**
- Widget iOS → texte ou voix → validation → écran vide
- Temps de capture: **< 5 secondes**

**Agent IA intelligent (Phase 2+):**
- Classification automatique (TODO, Idées, Notes)
- Merge intelligent de notes similaires
- Enrichissement contextuel

**Retrieval optimisé:**
- Recherche sémantique rapide
- Filtres intelligents par catégorie
- Vue chronologique et thématique

### 1.4 Critère de Succès Personnel

> **"Dans 30 jours, j'ouvre Flux 10x/jour minimum et je n'utilise plus Apple Notes"**

---

## 2. Objectifs

### 2.1 Objectifs Business

| Objectif | Métrique | Cible (3 mois) |
|----------|----------|----------------|
| Adoption personnelle | Captures/jour | ≥ 7 |
| Rétention | Jours d'utilisation consécutifs | ≥ 30 |
| Remplacement | % sessions via Flux vs autres apps | ≥ 80% |

### 2.2 Objectifs Produit

- **Vitesse absolue:** Capture en < 5 secondes du widget à la validation
- **Zéro friction:** Aucune décision requise pendant la capture
- **Fiabilité:** 99.9% des captures sauvegardées avec succès
- **Retrieval efficace:** Retrouver une note en < 10 secondes

### 2.3 Objectifs Techniques

- Widget launch time: < 200ms
- Classification IA: < 3 secondes (async)
- Search performance: < 100ms pour résultats
- Offline-first: fonctionne sans connexion

---

## 3. Personas & Use Cases

### 3.1 Primary Persona: Tom (Self)

**Profil:**
- 28 ans, Technical Account Manager chez Kameleoon
- Multiples projets simultanés (work, side projects, learning)
- Suspicion de ADHD/troubles attentionnels
- Utilise actuellement: Apple Notes, Todoist, papier éphémère

**Pain Points:**
- Oublie 50%+ des idées/tâches qui émergent
- Se sent submergé par la charge mentale
- Abandonne les systèmes trop complexes
- Frustration de ne pas retrouver ses notes

**Behaviors:**
- Pense à 15 choses simultanément
- Passe rapidement d'un sujet à l'autre
- Forte curiosité technique, tendance au perfectionnisme
- Préfère action immédiate vs planification

### 3.2 Use Cases Prioritaires

#### UC1: Quick Brain Dump
**Contexte:** Idée soudaine pendant réunion client  
**Action:** Ouvre widget → "Checker regex Cultura pour product grid" → Done  
**Résultat:** Idée capturée, esprit libre, focus retrouvé

#### UC2: Voice Capture en Mobilité
**Contexte:** Idée business dans le métro  
**Action:** Widget → bouton micro → "App pour automatiser tests A/B avec agents IA" → Done  
**Résultat:** Pas besoin de sortir téléphone ou taper

#### UC3: Recherche Rapide
**Contexte:** Dimanche soir, préparation semaine  
**Action:** Open app → Search "Kameleoon" → voit toutes les notes work  
**Résultat:** Retrouve le contexte en 10 secondes

#### UC4: Revue Hebdomadaire
**Contexte:** Fin de semaine, organiser les idées  
**Action:** Filter "IDEA" + "Cette semaine" → scroll → triage  
**Résultat:** Décide quelles idées explorer, supprimer, ou archiver

---

## 4. Scope MVP

### 4.1 Phase 1: MVP Core (3 semaines)

#### MUST HAVE ✅

**Capture:**
- [ ] Widget iOS avec input direct (text + voice)
- [ ] Placeholder intelligent: "Écris ou parle..."
- [ ] Voice-to-text natif (Speech Framework)
- [ ] Validation auto après 3 sec inactivité OU bouton explicit "Done"
- [ ] Haptic feedback à la validation
- [ ] Écran redevient vide après capture
- [ ] Support offline (queue locale si pas de réseau)

**Storage:**
- [ ] SQLite local avec Core Data
- [ ] Schema: id, content, category, created_at, source, is_deleted
- [ ] Full-text search index (FTS5)

**Classification:**
- [ ] API Anthropic (Claude Haiku) pour classification
- [ ] 3 catégories: TODO, IDEA, NOTE
- [ ] Classification async (non-bloquante)
- [ ] Fallback si API fail: tag "NOTE" par défaut
- [ ] Retry logic: 1 retry max, puis fallback

**Retrieval:**
- [ ] Liste reverse chronological
- [ ] Tabs: All / TODO / IDEA / NOTE
- [ ] Search bar avec full-text search
- [ ] Tap note → vue détail
- [ ] Swipe to delete

**UX/UI:**
- [ ] Design minimaliste, focus sur vitesse
- [ ] Dark mode native
- [ ] Animations fluides (< 60fps)
- [ ] Pas de notifications (volontairement)

#### NICE TO HAVE (Phase 1) 🔶

- [ ] Filter par date (aujourd'hui, cette semaine, ce mois)
- [ ] Compteur de captures dans widget
- [ ] Export CSV basique
- [ ] Undo delete (5 secondes grace period)

---

### 4.2 Phase 2: Agent Intelligent (Après validation MVP)

**Merge automatique:**
- Agent détecte notes similaires et propose merge
- Historique des merges visible
- Undo possible

**Enrichissement:**
- Ajout métadata automatique (liens, dates extraites, etc.)
- Suggestions de tags
- Détection patterns (ex: "Tu penses souvent à X ces temps-ci")

**Recherche sémantique:**
- Recherche par similarité (embeddings)
- "Trouve mes notes sur l'automatisation" → résultats même si mot exact absent

**Intégrations:**
- Todoist/Things pour export TODOs
- Calendar pour events détectés
- Notion/Obsidian pour notes longues

---

## 5. User Flows

### 5.1 Flow 1: Capture Ultra-Rapide (Critique)

```
État: Home screen (iOS)
│
├─> [SWIPE] Widget Flux apparait
│   │
│   ├─> [AUTO] Curseur clignote dans input
│   │
│   ├─> [USER] Tape OU parle
│   │   │
│   │   ├─> Option A: Tape "Idée: app notes ADHD"
│   │   │
│   │   └─> Option B: Tap micro → parle "Idée app notes ADHD"
│   │
│   ├─> [AUTO] 3 secondes inactivité OU tap "Done"
│   │
│   ├─> [SYSTEM] Haptic feedback subtle
│   │   │
│   │   ├─> Sauvegarde locale instantanée
│   │   │
│   │   └─> Classification IA (async, background)
│   │
│   └─> [AUTO] Widget disparait, input se vide
│
└─> État: Home screen (retour à la normale)
```

**Timing goal:** < 5 secondes total (de swipe à disparition)

---

### 5.2 Flow 2: Retrouver une Note

```
État: Besoin de retrouver quelque chose
│
├─> [USER] Open app Flux
│   │
│   ├─> [SCREEN] Liste des captures (reverse chrono)
│   │   │
│   │   ├─> Option A: Scroll dans tab "All"
│   │   │
│   │   ├─> Option B: Switch tab "IDEA" / "TODO" / "NOTE"
│   │   │
│   │   └─> Option C: Tap search → tape "Kameleoon"
│   │       │
│   │       └─> [AUTO] Résultats filtrés instantanément
│   │
│   ├─> [USER] Tap sur une note
│   │   │
│   │   └─> [SCREEN] Détail note (full content, metadata)
│   │
│   └─> Options:
│       │
│       ├─> Swipe left → Delete
│       │
│       ├─> Tap "Edit" → Modifier contenu
│       │
│       └─> Back → Retour liste
```

---

### 5.3 Flow 3: Revue Hebdomadaire

```
État: Dimanche soir, review de la semaine
│
├─> [USER] Open app Flux
│   │
│   ├─> [USER] Tap filter icon
│   │   │
│   │   └─> Sélectionne "Cette semaine"
│   │
│   ├─> [USER] Switch tab "IDEA"
│   │
│   ├─> [SCREEN] Liste toutes les IDEAS de la semaine
│   │
│   └─> Pour chaque note:
│       │
│       ├─> Keep (rien faire)
│       │
│       ├─> Delete (swipe)
│       │
│       └─> [Phase 2] "Promote to Project"
```

---

## 6. Spécifications Techniques

### 6.1 Tech Stack

**Frontend:**
- Swift 5.9+
- SwiftUI (iOS 17+)
- WidgetKit pour widget
- Speech Framework pour voice-to-text

**Backend:**
- Aucun backend pour MVP (local-first)
- API Anthropic (classification uniquement)

**Storage:**
- SQLite (Core Data wrapper)
- Full-text search: FTS5

**Tooling:**
- Xcode 15+
- Swift Package Manager
- TestFlight pour beta

---

### 6.2 Data Model

#### Schema SQLite

```sql
-- Table principale
CREATE TABLE IF NOT EXISTS captures (
    id TEXT PRIMARY KEY,              -- UUID
    content TEXT NOT NULL,            -- Texte capturé
    category TEXT CHECK(category IN ('TODO', 'IDEA', 'NOTE')),
    created_at INTEGER NOT NULL,      -- Unix timestamp
    updated_at INTEGER,               -- Pour tracking modifications
    source TEXT CHECK(source IN ('text', 'voice')),
    is_deleted INTEGER DEFAULT 0,    -- Soft delete
    classification_status TEXT CHECK(classification_status IN ('pending', 'done', 'failed')),
    raw_voice_text TEXT              -- Si voice, texte brut avant processing
);

-- Index pour performance
CREATE INDEX idx_created_at ON captures(created_at DESC);
CREATE INDEX idx_category ON captures(category);
CREATE INDEX idx_deleted ON captures(is_deleted);

-- Full-text search
CREATE VIRTUAL TABLE captures_fts USING fts5(
    content,
    content=captures,
    content_rowid=id
);

-- Triggers pour sync FTS
CREATE TRIGGER captures_ai AFTER INSERT ON captures BEGIN
    INSERT INTO captures_fts(rowid, content) VALUES (new.id, new.content);
END;

CREATE TRIGGER captures_ad AFTER DELETE ON captures BEGIN
    DELETE FROM captures_fts WHERE rowid = old.id;
END;

CREATE TRIGGER captures_au AFTER UPDATE ON captures BEGIN
    UPDATE captures_fts SET content = new.content WHERE rowid = new.id;
END;
```

---

### 6.3 Classification IA

#### API Call Structure

**Endpoint:** Anthropic Messages API  
**Model:** `claude-haiku-4-20250514`  
**Max tokens:** 10 (on veut juste TODO/IDEA/NOTE)

**Prompt:**

```
Classify this user note into ONE category only.

Categories:
- TODO: Actions, tasks, things to do, reminders, shopping lists
- IDEA: Projects, concepts, business ideas, creative thoughts, learning topics
- NOTE: Everything else (observations, references, journal entries, thoughts)

Note: "{user_input}"

Response format: Return ONLY the category name (TODO, IDEA, or NOTE), nothing else.
```

**Example Inputs/Outputs:**

```
Input: "Acheter du lait"
Output: TODO

Input: "Idée app de notes pour ADHD"
Output: IDEA

Input: "Le dernier film de Nolan est incroyable"
Output: NOTE

Input: "Checker regex Cultura product grid"
Output: TODO

Input: "Explorer Rust pour backend"
Output: IDEA
```

#### Error Handling

```swift
func classifyCapture(_ text: String) async -> Category {
    do {
        let response = try await anthropicAPI.classify(text)
        return Category(rawValue: response) ?? .note
    } catch {
        // Log error pour debugging
        logger.error("Classification failed: \(error)")
        
        // Retry logic
        if retryCount < 1 {
            retryCount += 1
            return await classifyCapture(text)
        }
        
        // Fallback: utiliser classification locale simple
        return fallbackClassify(text)
    }
}

func fallbackClassify(_ text: String) -> Category {
    let todoKeywords = ["acheter", "rappeler", "checker", "faire", "todo"]
    let ideaKeywords = ["idée", "projet", "explorer", "app", "startup"]
    
    let lowercased = text.lowercased()
    
    if todoKeywords.contains(where: { lowercased.contains($0) }) {
        return .todo
    }
    
    if ideaKeywords.contains(where: { lowercased.contains($0) }) {
        return .idea
    }
    
    return .note
}
```

---

### 6.4 Performance Requirements

| Métrique | Target | Critique? |
|----------|--------|-----------|
| Widget launch | < 200ms | ✅ OUI |
| Capture save (local) | < 50ms | ✅ OUI |
| Classification API | < 3s | ⚠️ Non-bloquant |
| Search results | < 100ms | ✅ OUI |
| List scroll (60fps) | 16.67ms/frame | ✅ OUI |
| App cold start | < 1s | 🔶 Nice to have |

---

### 6.5 Architecture

```
┌─────────────────────────────────────────┐
│           Widget Extension              │
│  ┌──────────────────────────────────┐   │
│  │  Input View (Text + Voice)       │   │
│  │  - Minimal UI                    │   │
│  │  - Direct save to shared DB      │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
                    │ Save
                    ▼
┌─────────────────────────────────────────┐
│         Shared Data Container           │
│  ┌──────────────────────────────────┐   │
│  │  SQLite Database                 │   │
│  │  - captures table                │   │
│  │  - FTS index                     │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
                    │ Read/Write
                    ▼
┌─────────────────────────────────────────┐
│            Main App                     │
│  ┌──────────────────────────────────┐   │
│  │  Repository Layer                │   │
│  │  - CRUD operations               │   │
│  │  - Search logic                  │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  Classification Service          │   │
│  │  - API calls (async)             │   │
│  │  - Retry logic                   │   │
│  │  - Fallback classification       │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  UI Layer (SwiftUI)              │   │
│  │  - List view                     │   │
│  │  - Search view                   │   │
│  │  - Detail view                   │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
                    │ Background queue
                    ▼
┌─────────────────────────────────────────┐
│       Classification Queue              │
│  - Process pending captures             │
│  - Update categories                    │
│  - Retry failures                       │
└─────────────────────────────────────────┘
```

---

## 7. Design & UX

### 7.1 Principes de Design

1. **Speed-first:** Chaque interaction optimisée pour vitesse
2. **Zero-chrome:** UI minimale, pas de distractions
3. **Forgiveness:** Undo facile, pas de confirmations inutiles
4. **Invisible intelligence:** IA travaille en background, transparente

### 7.2 Color Palette

**Primary:**
- Background: `#0A0A0A` (noir profond)
- Surface: `#1C1C1E` (gris très foncé)
- Input: `#2C2C2E` (gris moyen)

**Accents:**
- Primary: `#8E7FE5` (lavande - du concept Capture)
- Success: `#34C759` (vert iOS)
- Warning: `#FF9500` (orange iOS)
- Error: `#FF3B30` (rouge iOS)

**Text:**
- Primary: `#FFFFFF`
- Secondary: `#8E8E93`
- Tertiary: `#48484A`

**Categories:**
- TODO: `#FF9500` (orange - action)
- IDEA: `#8E7FE5` (lavande - créativité)
- NOTE: `#8E8E93` (gris - neutre)

### 7.3 Typography

- **System Font:** SF Pro (natif iOS)
- **Input:** SF Pro Regular, 17pt
- **List items:** SF Pro Regular, 16pt
- **Metadata:** SF Pro Regular, 14pt (secondary color)

### 7.4 Key Screens (Wireframe Description)

#### Widget (Compact)
```
┌────────────────────────┐
│  Écris ou parle...     │ ← Placeholder
│  [                  ]  │ ← Input area
│                    Done│ ← Button (si texte saisi)
└────────────────────────┘
```

#### Main App - List View
```
┌────────────────────────────────┐
│  ☰ Flux           🔍           │ ← Header
├────────────────────────────────┤
│  All  TODO  IDEA  NOTE         │ ← Tabs
├────────────────────────────────┤
│ ● Idée app notes ADHD          │
│   il y a 2 heures · IDEA       │
├────────────────────────────────┤
│ ● Checker regex Cultura        │
│   il y a 5 heures · TODO       │
├────────────────────────────────┤
│ ● Film Nolan incroyable        │
│   hier · NOTE                  │
└────────────────────────────────┘
```

#### Detail View
```
┌────────────────────────────────┐
│  ← Back              🗑️         │
├────────────────────────────────┤
│  Idée app notes ADHD           │ ← Title (content)
│                                │
│  14 Jan 2026, 14:32           │ ← Metadata
│  Catégorie: IDEA               │
│  Source: Voice                 │
│                                │
│  [Edit]                        │ ← Action
└────────────────────────────────┘
```

---

## 8. Success Metrics

### 8.1 Adoption Metrics (30 jours)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Captures totales | ≥ 200 | Tracking local |
| Captures/jour (moyenne) | ≥ 7 | Analytics |
| % via widget vs app | ≥ 80% | Source tracking |
| % voice vs text | ≥ 50% | Source tracking |
| Jours consécutifs utilisation | ≥ 30 | Retention |

### 8.2 Engagement Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Sessions search/semaine | ≥ 3 | Feature usage |
| Taux de suppression | < 20% | Indicator utilité |
| Notes retrouvées en <10s | ≥ 90% | UX quality |
| Temps moyen de capture | < 5s | Performance |

### 8.3 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Classification accuracy | ≥ 85% | Manual audit |
| Crash rate | < 0.1% | Xcode analytics |
| API success rate | ≥ 95% | Error logging |
| Widget launch time | < 200ms | Performance tracking |

### 8.4 Subjective Success (Personal)

**Questions à se poser après 30 jours:**

- [ ] Est-ce que j'oublie moins de choses importantes?
- [ ] Est-ce que ma charge mentale a diminué?
- [ ] Est-ce que je retrouve facilement mes notes?
- [ ] Est-ce que j'ai abandonné mes autres apps de notes?
- [ ] Est-ce que l'app me frustre ou me rend service?

**Decision tree:**
- **5/5 OUI** → Continue, passe en Phase 2
- **3-4 OUI** → Itère sur MVP, identifie blockers
- **<3 OUI** → Pivot ou abandon

---

## 9. Out of Scope

### 9.1 Explicitement HORS MVP

❌ **Collaboration:**
- Partage de notes
- Modes multi-utilisateurs
- Commentaires/threads

❌ **Formatting avancé:**
- Markdown editor
- Rich text (bold, italics, etc.)
- Attachments (images, files)
- Dessins/sketches

❌ **Organisation complexe:**
- Tags customs
- Folders/collections
- Hierarchies
- Liens entre notes

❌ **Automatisation poussée:**
- Merge automatique (Phase 2)
- Suggestions proactives
- Rappels/notifications
- Récurrence

❌ **Intégrations:**
- Todoist, Notion, Calendar (Phase 2)
- Export avancé (PDF, etc.)
- Import depuis autres apps

❌ **Social/Discovery:**
- Templates publics
- Marketplace
- Communauté

❌ **Multi-platform:**
- Web app
- Android
- macOS native
- (Sync iOS uniquement pour MVP)

---

## 10. Risks & Mitigations

### 10.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API Anthropic indisponible | Medium | High | Fallback classification locale + retry logic |
| Widget trop lent (>200ms) | Medium | Critical | Profiling précoce, optimisations launch time |
| Voice-to-text imprécis | High | Medium | Permettre edit immédiat post-capture |
| SQLite corruption | Low | Critical | Backups automatiques, export régulier |
| Battery drain (classifications) | Low | Medium | Queue intelligente, batching des API calls |

### 10.2 Product Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Abandon après 1 semaine | Medium | Critical | Commitment personnel, tracking daily |
| Classification IA mauvaise | Medium | High | Manual audit régulier, amélioration prompt |
| Trop de friction résiduelle | Medium | High | User testing continu (dogfooding) |
| Ne résout pas vraiment ADHD | Low | Critical | Validation use cases réels quotidiennement |

### 10.3 Business Risks (Phase 2+)

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Marché trop niche | High | Medium | Commencer ultra-niche, élargir progressivement |
| Concurrence (Mem.ai, etc.) | High | Medium | Focus sur vitesse/ADHD, pas general-purpose |
| Coût API (scale) | Medium | High | Modèle freemium, classifications locales |

---

## 11. Timeline

### 11.1 Phase 1: MVP Development (3 semaines)

#### Semaine 1: Foundation
**Jours 1-2:**
- [ ] Setup Xcode project (iOS 17+, Swift 5.9)
- [ ] Configure Widget extension
- [ ] Setup SQLite + Core Data models
- [ ] Create database schema + migrations

**Jours 3-5:**
- [ ] Implement basic text input dans widget
- [ ] Save to SQLite (CRUD operations)
- [ ] Basic main app: liste des captures
- [ ] Navigation: liste → détail

**Jours 6-7:**
- [ ] Delete functionality (swipe)
- [ ] Full-text search (FTS5)
- [ ] Tabs (All/TODO/IDEA/NOTE)

---

#### Semaine 2: Intelligence & Voice
**Jours 8-10:**
- [ ] Integration API Anthropic
- [ ] Classification service (async)
- [ ] Retry logic + fallback
- [ ] Background queue processing

**Jours 11-12:**
- [ ] Voice-to-text (Speech Framework)
- [ ] Micro button dans widget
- [ ] Permission handling
- [ ] Error states

**Jours 13-14:**
- [ ] Auto-validation (3 sec inactivité)
- [ ] Haptic feedback
- [ ] Widget animations
- [ ] Polish UX

---

#### Semaine 3: Polish & Testing
**Jours 15-17:**
- [ ] Dark mode polish
- [ ] Performance optimizations
- [ ] Error handling complet
- [ ] Edge cases (offline, etc.)

**Jours 18-19:**
- [ ] Beta testing (TestFlight)
- [ ] Bug fixes critiques
- [ ] Analytics setup (basic)
- [ ] Documentation

**Jour 20-21:**
- [ ] Final polish
- [ ] Release MVP interne
- [ ] Commit: utiliser uniquement Flux pendant 30 jours

---

### 11.2 Phase 2: Post-MVP (si validation)

**Semaine 4-5: Dogfooding intensif**
- Utilisation quotidienne exclusive
- Bug tracking
- Feature requests prioritization
- Metrics analysis

**Semaine 6-8: Agent Intelligent** (si validation metrics)
- Merge automatique
- Enrichissement notes
- Recherche sémantique

**Semaine 9-12: Intégrations** (si retention >30 jours)
- Todoist/Things
- Calendar
- Export avancé

---

## 12. Open Questions

### 12.1 Naming & Branding
- [ ] Nom final: "Flux" définitif ou brainstorm alternatives?
- [ ] App icon: design maison ou designer externe?
- [ ] Tagline exact pour App Store (si public un jour)

### 12.2 UX Details
- [ ] Gesture pour delete: swipe left uniquement ou long-press aussi?
- [ ] Confirmation avant delete ou undo immédiat (iOS style)?
- [ ] Placeholder text: "Écris ou parle" vs alternatives?
- [ ] Animations: durée exacte, courbes (ease-in-out)?

### 12.3 Technical Decisions
- [ ] Comportement si classification échoue 3x de suite?
  - Option A: Rester en "pending" indéfiniment
  - Option B: Force fallback après 3 tentatives
  - **Décision:** TBD
  
- [ ] Stratégie backup/export:
  - Option A: Export manuel CSV
  - Option B: iCloud backup automatique
  - **Décision:** Manuel pour MVP, auto en Phase 2

- [ ] Dark mode uniquement ou light mode aussi?
  - **Décision:** Dark mode only pour MVP (target audience + économie batterie OLED)

### 12.4 Monetization (Post-MVP)
- [ ] Freemium: limite de captures/mois?
- [ ] Premium: quelles features payantes?
- [ ] One-time purchase vs subscription?
- **Note:** Pas de monetization en Phase 1, décision après validation

### 12.5 Privacy & Data
- [ ] Mention explicite: "Tes notes sont analysées par IA" dans onboarding?
- [ ] Option opt-out classification (tout reste local)?
- [ ] Export/delete all data (RGPD compliance)?
- **Décision:** Transparence totale dès MVP

---

## Appendix

### A. Références & Inspirations

**Apps similaires analysées:**
- Mem.ai (AI-native notes, search sémantique)
- Reflect Notes (networked thought, backlinking)
- Drafts (quick capture, actions)
- Google Keep (simplicité, voice)

**Différenciateurs Flux:**
- Vitesse absolue (widget ultra-rapide)
- ADHD-first design
- Agent IA qui maintient structure (pas juste search)
- Pas de folders/tags manuels

### B. Resources

**Documentation:**
- [WidgetKit - Apple Developer](https://developer.apple.com/documentation/widgetkit)
- [Speech Framework - Apple](https://developer.apple.com/documentation/speech)
- [Core Data - Apple](https://developer.apple.com/documentation/coredata)
- [Anthropic API - Messages](https://docs.anthropic.com/en/api/messages)

**Tools:**
- Xcode 15+
- TestFlight (beta distribution)
- Anthropic Console (API keys, monitoring)

### C. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 14 Jan 2026 | Tom | Initial PRD - MVP scope |

---

## Contact & Feedback

**Product Owner:** Tom  
**Status:** Active Development - MVP Phase  
**Last Updated:** 14 Janvier 2026

**Next Review:** Après 30 jours d'utilisation (mi-février 2026)

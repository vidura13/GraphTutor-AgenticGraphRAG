# ADR-0001: Graph-forking = canonical graph + private overlays

- **Status**: PROPOSED (sign-off: M01+M02 in S0; freeze in S5)
- **Context**: peers must share curriculum structure without duplicating storage; individual BKT
  states must stay mathematically isolated (proposal §1.3, §4.2).
- **Decision**: one canonical curriculum graph; sharing = ACL row in PostgreSQL granting read on
  `curriculum_{id}`; per-user mastery only in Postgres; per-user vectors in Chroma collection
  `user_{id}_private`; personal annotations as `(:PersonalNote {owner})` overlays.
- **Rejected alternative**: copy-on-write subgraph forks (violates dedup/storage claim, sync hell).
- **Consequences**: M01 schema carries `owner`/ACL seams; M02 implements ACL endpoints;
  M03 never reads another user's rows; M04 heatmap joins snapshot + own mastery only.

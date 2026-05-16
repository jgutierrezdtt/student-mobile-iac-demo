# Medalla de completacion — template-secure-coding-mobile-iac

**Token de integridad:** `F6AE04903850F9D8BDAD8C9BE827CC75E13FBD39`

| Campo | Valor |
|-------|-------|
| Repositorio | `jgutierrezdtt/template-secure-coding-mobile-iac` |
| Completado por | `jgutierrezdtt` |
| Pasos verificados | 10 de 10 |
| Fecha | 2026-05-16 20:29 UTC |
| Verifier Run ID | `25972133838` |

---

## Que garantiza este token

- Los 10 validators fueron ejecutados por `jgutierrezdtt/tutorial-verifier`, un repositorio controlado por el instructor, **no por el alumno**.
- El codigo verificado es el que estaba en el fork en el momento de la solicitud — el verifier hizo `git clone` del fork directamente.
- El token es HMAC-SHA256 firmado con `COMPLETION_SECRET`, un secreto que existe **unicamente** en el repositorio del verifier. El alumno nunca puede leerlo ni calcularlo.
- El `Verifier Run ID` (`25972133838`) es el ID de la ejecucion de Actions en el verifier. Puedes auditarlo en `https://github.com/jgutierrezdtt/tutorial-verifier/actions/runs/25972133838`.
- Modificar este archivo manualmente invalida el token — `verify-medal.py` en el fork detecta la manipulacion en cada push.

---

## Como auditar esta completacion

1. Abre `https://github.com/jgutierrezdtt/tutorial-verifier/actions/runs/25972133838`
2. Comprueba los logs del job `Verify jgutierrezdtt/template-secure-coding-mobile-iac`.
3. Todos los validators deben aparecer como `PASS`.
4. El token en los logs debe coincidir con el token de arriba.

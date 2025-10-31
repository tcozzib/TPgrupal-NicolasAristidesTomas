
Hola chicos!
Acá dejo el repo con el template y la consigna para que vayamos modificando. Si prefieren, hacemos una sola branch, pero si quieren hacer cada uno la suya y después vemos cómo resolvemos los merges para unificar.
Este archivo también lo modificamos para que quede como portada del tp o algo más presentable que este mensaje.
Saludos. 

## Ramas y merge (resumen rápido)
Cada integrante puede trabajar en su propia rama y luego unir los cambios a `main`. Recomendado: usar Pull Requests para revisión.

1) Crear una rama nueva local y hacer push al remoto

```powershell
git checkout -b feature/tu-nombre
# editar archivos, luego:
git add .
git commit -m "Descripción breve de los cambios"
git push -u origin feature/tu-nombre
```

2) Mantener tu rama actualizada con `main` (antes de abrir PR o merge)

```powershell
git checkout main
git pull --rebase origin main
git checkout feature/tu-nombre
git rebase main
# resolver conflictos si aparecen, luego:
git push --force-with-lease origin feature/tu-nombre
```

3) Abrir un Pull Request (recomendado)

Opción web: Ir a GitHub → tu repo → Compare & pull request.

Opción CLI:

```powershell
gh pr create --base main --head feature/tu-nombre --title "Mi PR" --body "Descripción breve"
```

4) Mergear a `main` (después de revisión)

Opción web: usar el botón Merge en el Pull Request.

Opción CLI (merge y borrar la rama remota):

```powershell
gh pr merge --merge --delete-branch --repo tcozzib/TPgrupal-NicolasAristidesTomas --head feature/tu-nombre
```

5) Mergear localmente (si prefieren hacerlo por terminal sin PR)

```powershell
git checkout main
git pull --rebase origin main
git merge --no-ff feature/tu-nombre -m "Merge feature/tu-nombre"
git push origin main
# borrar la rama local y remota si ya no se usa:
git branch -d feature/tu-nombre
git push origin --delete feature/tu-nombre
```

Si quieren, puedo añadir una breve guía con convención de nombres de ramas y un template de PR en el repo.


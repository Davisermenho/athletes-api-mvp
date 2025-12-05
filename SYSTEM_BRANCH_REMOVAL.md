# Remoção da branch `system` e envio de novos arquivos

Caso precise limpar o histórico da branch `system` e trabalhar apenas com a branch atual (`work`), siga estes passos:

1. Verifique se a branch `system` existe localmente. Caso exista, exclua-a:
   ```bash
   git branch -D system
   ```
2. Remova a referência remota (se houver):
   ```bash
   git push origin --delete system
   ```
3. Garanta que está na branch de trabalho:
   ```bash
   git checkout work
   ```
4. Adicione os novos arquivos ou alterações desejadas e faça o commit:
   ```bash
   git add <novos-arquivos-ou-pastas>
   git commit -m "Adiciona novos arquivos após remoção da branch system"
   ```
5. Envie as mudanças para o remoto:
   ```bash
   git push origin work
   ```

> Observação: se a branch `system` não existir mais no repositório, apenas ignore as etapas de exclusão e siga adicionando os novos arquivos.

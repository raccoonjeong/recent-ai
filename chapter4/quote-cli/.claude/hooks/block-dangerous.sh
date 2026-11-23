#!/bin/bash
set -euo pipefail
input="$(cat)" # 1. 표준 입력으로 들어온 JSON 찾기
command="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')" # 2. 실행될 셀 명령 추출

# 3. rm -rf 계열(옵션 순서 변형 포함)인지 검사
if printf '%s' "$command" | grep -Eq 'rm[[:space:]]+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)'; then
  # 4. 위험 명령이면 차단 결정을 JSON으로 출력
  jq -n '{
    hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "재귀 강제 삭제(rm -rf)는 차단됩니다. 필요하면 대상 경로를 명시해 직접 실행해주세요."
    }
  }'
fi
exit 0 # 5. 패턴이 없으면 통과
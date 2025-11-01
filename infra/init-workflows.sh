#!/bin/sh

# n8n이 백그라운드로 시작
echo "Starting n8n in background..."
n8n start &
N8N_PID=$!

# n8n 서버가 준비될 때까지 대기
echo "Waiting for n8n to be ready..."
max_retries=60
retry_count=0

while [ $retry_count -lt $max_retries ]; do
  if wget -q -O- http://localhost:5678/healthz > /dev/null 2>&1; then
    echo "n8n is ready!"
    sleep 5  # API가 완전히 준비되도록 추가 대기
    break
  fi
  retry_count=$((retry_count + 1))
  echo "Waiting for n8n... ($retry_count/$max_retries)"
  sleep 2
done

if [ $retry_count -eq $max_retries ]; then
  echo "ERROR: n8n failed to start"
  exit 1
fi

# workflows 폴더의 모든 JSON 파일 import
echo "Starting workflow import..."
for workflow_file in ./workflows/*.json; do
  if [ -f "$workflow_file" ]; then
    echo "Importing workflow: $(basename $workflow_file)"
    
    # N8N API를 사용한 workflow import (인증 비활성화 상태)
    response=$(wget -q -O- --post-file="$workflow_file" \
      --header="Content-Type: application/json" \
      http://localhost:5678/api/v1/workflows 2>&1)
    
    if [ $? -eq 0 ]; then
      echo "✓ Successfully imported: $(basename $workflow_file)"
    else
      echo "✗ Failed to import: $(basename $workflow_file)"
      echo "Error: $response"
    fi
  fi
done

echo "All workflows processed!"

# n8n을 foreground로 유지
wait $N8N_PID
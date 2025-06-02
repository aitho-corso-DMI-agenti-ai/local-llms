export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
export SERVICE_HOSTNAME="kserve-local-llm.kserve-test.example.com"

echo $INGRESS_HOST
echo $INGRESS_PORT
echo $SERVICE_HOSTNAME

curl -H "content-type:application/json" -H "Host: ${SERVICE_HOSTNAME}" \
    -v http://${INGRESS_HOST}:${INGRESS_PORT}/openai/v1/chat/completions \
    -d "$(cat payload.json)"

# curl -H "content-type:application/json" \
#     -H "Host: ${SERVICE_HOSTNAME}" \
#     -v \
#     "http://${INGRESS_HOST}:${INGRESS_PORT}" \



minikube kubectl -- delete namespace kserve-test
minikube kubectl -- create namespace kserve-test
envsubst < llm_schema.yml | minikube kubectl -- apply -f -
# minikube kubectl -- -n kserve-test rollout restart deploy kserve-local-llm

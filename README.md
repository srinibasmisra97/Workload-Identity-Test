# GKE Workload Identity Trial with SQL

Application is [here](./main.py).

Create basic secret for DB Credentials:
```bash
kubectl create secret generic db-credentials \
--from-literal=SQL_USER=demo \
--from-literal=SQL_HOST=127.0.0.1 \
--from-literal=SQL_PASSWORD=demopassword \
--from-literal=SQL_DATABASE=demo_db
```

## Approach 1 - Service Account JSON File as Secret

Deployment file is [here](./manifest.yaml).

Download service account key file:
```bash
gcloud iam service-accounts keys create key.json --iam-account demo-sql-sa@dev-trials-project.iam.gserviceaccount.com
```

This secret file would be mounted to the Cloud SQL Proxy from a secret volume.

## Approach 2 - Workload Identity

Deployment file is [here](./manifest-id.yaml).

[Docs](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine) followed.

Workload identity is a mechanism to add a Kubernetes service account as a member of a GCP service account. The pod would run as this Kubernetes service account.

Creating a Kubernetes service account:
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-sql-sa
  annotations:
    iam.gke.io/gcp-service-account: demo-sql-sa@dev-trials-project.iam.gserviceaccount.com
```

Adding Kubernetes service account as a member to GCP service account:
```bash
gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:dev-trials-project.svc.id.goog[default/demo-sql-sa]" \
  demo-sql-sa@dev-trials-project.iam.gserviceaccount.com
```
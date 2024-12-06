from fastapi import FastAPI
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml
import subprocess
import logging

#logging config
logging.basicConfig(level=logging.DEBUG)

# Load the Kubernetes config (local setup or in-cluster if running within the cluster)
config.load_kube_config()  


app = FastAPI()

#health status
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/", tags=["home"])
async def root():
    logging.info("Root endpoint accessed")
    return {'status':'ok 👍🐍 '}


@app.post("/trigger-job/")
async def trigger_k8s_job():
    # Load the job YAML file
    with open("producer-job.yaml", "r") as file:
        job_manifest = yaml.safe_load(file)
    
    try:
        # Get the Kubernetes API client for batch jobs
        batch_v1 = client.BatchV1Api()
        
        # Create the job
        batch_v1.create_namespaced_job(namespace="default", body=job_manifest)
        return {"message": "Job triggered successfully!"}
    
    except ApiException as e:
        return {"error": f"Error creating job: {e}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

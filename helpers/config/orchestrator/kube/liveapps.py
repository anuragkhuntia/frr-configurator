import logging
from kubernetes import client, config, watch

# Configure logging
logging.basicConfig(
    format='{"timestamp":"%(asctime)s","log_level":"%(levelname)s","message":"%(message)s","app":"%(name)s"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
)

logger = logging.getLogger("KubernetesEventWatcher")


class KubernetesEventWatcher:
    def __init__(self, namespace="default"):
        self.namespace = namespace
        self.v1 = None
        self.apps_v1 = None
        self.watcher = watch.Watch()

    def load_config(self):
        try:
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes config")
        except config.ConfigException:
            config.load_kube_config()
            logger.info("Loaded kube config from local")

        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def watch_events(self):
        logger.info(f"Watching events in namespace: {self.namespace}")
        try:
            for event in self.watcher.stream(self.v1.list_namespaced_event, self.namespace):
                logger.info(
                    f"[{event['type']}] {event['object'].involved_object.kind} "
                    f"{event['object'].involved_object.name}: {event['object'].message}"
                )
        except KeyboardInterrupt:
            logger.info("Stopping event watcher...")
            self.watcher.stop()
        except Exception as e:
            logger.error(f"Error: {e}")

    def watch_deployment_events(self, deployment_name):
        logger.info(f"Watching events for deployment: {deployment_name} in namespace: {self.namespace}")
        try:
            for event in self.watcher.stream(self.v1.list_namespaced_event, self.namespace):
                involved_object = event['object'].involved_object
                if involved_object.kind == "Deployment" and involved_object.name == deployment_name:
                    logger.info(
                        f"[{event['type']}] {involved_object.kind} {involved_object.name}: {event['object'].message}"
                    )
        except KeyboardInterrupt:
            logger.info("Stopping deployment event watcher...")
            self.watcher.stop()
        except Exception as e:
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    namespace = "default"
    deployment_name = "your-deployment-name"

    watcher = KubernetesEventWatcher(namespace)
    watcher.load_config()

    # watcher.watch_events()
    # watcher.watch_deployment_events(deployment_name)

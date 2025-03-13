from kubernetes import client, config, watch

class KubernetesEventWatcher:
    def __init__(self, namespace="default"):
        self.namespace = namespace
        self.v1 = None
        self.apps_v1 = None
        self.watcher = watch.Watch()

    def load_config(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def watch_events(self):
        print(f"Watching events in namespace: {self.namespace}")
        try:
            for event in self.watcher.stream(self.v1.list_namespaced_event, self.namespace):
                print(f"[{event['type']}] {event['object'].involved_object.kind} {event['object'].involved_object.name}: {event['object'].message}")
        except KeyboardInterrupt:
            print("Stopping event watcher...")
            self.watcher.stop()
        except Exception as e:
            print(f"Error: {e}")

    def watch_deployment_events(self, deployment_name):
        print(f"Watching events for deployment: {deployment_name} in namespace: {self.namespace}")
        try:
            for event in self.watcher.stream(self.v1.list_namespaced_event, self.namespace):
                involved_object = event['object'].involved_object
                if involved_object.kind == "Deployment" and involved_object.name == deployment_name:
                    print(f"[{event['type']}] {involved_object.kind} {involved_object.name}: {event['object'].message}")
        except KeyboardInterrupt:
            print("Stopping deployment event watcher...")
            self.watcher.stop()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    namespace = "default" 
    deployment_name = "your-deployment-name"  
    
    watcher = KubernetesEventWatcher(namespace)
    watcher.load_config()

    # watcher.watch_events()
    # watcher.watch_deployment_events(deployment_name)
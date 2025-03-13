from kubernetes import client, config, watch
import logging, os

class KubernetesEventWatcher:
    logging.basicConfig(
        format='{\"timestamp\":\"%(asctime)s\",\"log_level\":\"%(levelname)s\",\"message\":\"%(message)s\",\"app\":\"%(name)s\"}',
        level=logging.INFO,
        datefmt='%Y-%m-%dT%H:%M:%S.000Z',
        )

    def __init__(self, namespace="default"):
        self.namespace = namespace
        self.v1 = None
        self.watcher = watch.Watch()

    def load_config(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        self.v1 = client.CoreV1Api() 

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

if __name__ == "__main__":
    namespace = "default"  # Change this to the desired namespace
    watcher = KubernetesEventWatcher(namespace)
    watcher.load_config()
    watcher.watch_events()
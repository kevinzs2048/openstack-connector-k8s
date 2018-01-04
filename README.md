Kubernetes connector for OpenStack.

Make OpenStack as a Node in Kubernetes to supply container service.
Mainly depending on OpenStack Zun project(container management service)

User will use Kubernetes API and running the pods on the Node which is the
really OpenStack Zun offers. 

Since there is a new project called: virtual-kubelet, we plan to reuse these
project to realize this function.

Now Zun is almostly ready to do several function for Capsule(Container Group),
which is a backend realization for Kubernetes pod.

Next step plan:
1. Implement the gophercloud for OpenStack Zun support.
2. Implement the OpenStack Zun support in virtual-kubelet.
3. Implement corresponding support in Zun project.

Ref:
1. Virtual-Kubelet: https://github.com/virtual-kubelet/virtual-kubelet
2. Gophercloud: https://github.com/gophercloud/gophercloud

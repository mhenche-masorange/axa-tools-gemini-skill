# Apigee Proxy XML Mapping

To find specific configuration values in an Apigee Proxy bundle (typically located in the `apiproxy/` directory):

## 1. Base Path
- **File**: `apiproxy/proxies/default.xml` (or any file in `apiproxy/proxies/`)
- **XPath**: `/ProxyEndpoint/HTTPProxyConnection/BasePath`

## 2. Target Timeouts
- **File**: `apiproxy/targets/default.xml` (or any file in `apiproxy/targets/`)
- **XPath**: `/TargetEndpoint/HTTPTargetConnection/Properties/Property`
- **Common Property Names**:
    - `io.timeout.millis`: Total time for the request/response.
    - `connect.timeout.millis`: Time to establish a connection.
    - `keepalive.timeout.millis`: Time to keep the connection alive.

## 3. Virtual Hosts
- **File**: `apiproxy/proxies/default.xml`
- **XPath**: `/ProxyEndpoint/HTTPProxyConnection/VirtualHost`

## 4. Policies
- **Location**: `apiproxy/policies/*.xml`
- **Quota**: Look for `<Quota>` element.
- **SpikeArrest**: Look for `<SpikeArrest>` element.

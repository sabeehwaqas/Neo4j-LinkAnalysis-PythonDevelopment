// File: hello.js

// Function to draw a NeoVis graph
function drawNeoVis() {
    const NEOVIS_ADVANCED_CONFIG = 'your_advanced_config_property_here'; // Define your advanced config property
    let neoViz;

    const config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "alinaqi",
            serverPassword: "12345678",
            database: "testingdb"
        },
        labels: {
            Character: {
                label: "name",
                value: "pagerank",
                group: "community",
                [NEOVIS_ADVANCED_CONFIG]: {
                    function: {
                        title: (node) => viz.nodeToHtml(node, [
                            "name",
                            "pagerank"
                        ])
                    }
                }
            }
        },
        relationships: {
            INTERACTS: {
                value: "weight"
            }
        },
        initialCypher: "MATCH (p:Person) RETURN p"
    };

    neoViz = new NeoVis.default(config);
    neoViz.render();
}

// Export the function so it can be used outside this file if needed
module.exports = {
    drawNeoVis: drawNeoVis
};

/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

/**
 * Procurement Dashboard Component
 */
export class ProcurementDashboard extends Component {
    static template = "procurement_management.Dashboard";

    setup() {
        this.state = {
            statistics: {},
            loading: true,
        };
        this.loadStatistics();
    }

    async loadStatistics() {
        try {
            const result = await this.env.services.rpc("/api/procurement/statistics");
            if (result.status === "success") {
                this.state.statistics = result.data;
            }
        } catch (error) {
            console.error("Error loading procurement statistics:", error);
        } finally {
            this.state.loading = false;
        }
    }
}

/**
 * Procedure Timeline Widget
 */
export class ProcedureTimeline extends Component {
    static template = "procurement_management.ProcedureTimeline";
    static props = {
        procedure: { type: Object },
    };

    get timelineSteps() {
        const steps = [
            { key: "draft", label: "Draft", icon: "fa-file" },
            { key: "published", label: "Published", icon: "fa-bullhorn" },
            { key: "open", label: "Open", icon: "fa-folder-open" },
            { key: "evaluation", label: "Evaluation", icon: "fa-balance-scale" },
            { key: "awarded", label: "Awarded", icon: "fa-trophy" },
        ];
        
        const currentIndex = steps.findIndex(s => s.key === this.props.procedure.state);
        return steps.map((step, index) => ({
            ...step,
            completed: index < currentIndex,
            current: index === currentIndex,
        }));
    }
}

/**
 * Bidder Score Display Widget
 */
export class BidderScoreWidget extends Component {
    static template = "procurement_management.BidderScoreWidget";
    static props = {
        technicalScore: { type: Number },
        financialScore: { type: Number },
        maxScore: { type: Number, optional: true },
    };

    get combinedScore() {
        const tech = this.props.technicalScore || 0;
        const fin = this.props.financialScore || 0;
        return ((tech * 0.7) + (fin * 0.3)).toFixed(2);
    }

    get technicalPercentage() {
        const max = this.props.maxScore || 100;
        return ((this.props.technicalScore || 0) / max * 100).toFixed(1);
    }

    get financialPercentage() {
        const max = this.props.maxScore || 100;
        return ((this.props.financialScore || 0) / max * 100).toFixed(1);
    }
}

// Register components
registry.category("actions").add("procurement_dashboard", ProcurementDashboard);

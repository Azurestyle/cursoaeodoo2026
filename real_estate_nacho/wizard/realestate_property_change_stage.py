from odoo import fields, models


class RealEstatePropertyChangeStage(models.TransientModel):
    _name = "realestate.property.change.stage"
    _description = "Wizard to change the stage of properties"

    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="Stage",
        required=True
    )

    def action_change_stage(self):
        properties = self.env["realestate.property"].browse(
            self.env.context.get("active_ids", [])
        )
        properties.write({"stage_id": self.stage_id.id})
        return {
            "type": "ir.actions.act_window",
            "name": "Properties",
            "res_model": "realestate.property",
            "view_mode": "kanban,list,pivot,graph,form",
            "domain": [("id", "in", properties.ids)],
            "target": "current",
        }

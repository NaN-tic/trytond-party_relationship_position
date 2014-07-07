from trytond.pool import PoolMeta
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['RelationPosition', 'PartyRelation', 'PartyRelationAll']
__metaclass__ = PoolMeta


class RelationPosition(ModelSQL, ModelView):
    'Relation Position'
    __name__ = 'party.relation.position'

    name = fields.Char('Name', required=True, translate=True)


class PartyRelation:
    __name__ = 'party.relation'

    position = fields.Many2One('party.relation.position', 'Position')


class PartyRelationAll(PartyRelation):
    __name__ = 'party.relation.all'
